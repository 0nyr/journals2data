import re

import pandas as pd
import numpy as np
from lxml import html
from sklearn.cluster import DBSCAN
from urllib.parse import urlparse

from .backpack import get_bagpack, get_attribute_list
from .build_xpath import to_xpath

from journals2data import data

def apply_DOM_prediction(
    dataframe: pd.DataFrame,
    source: data.Source
) -> pd.DataFrame:
    """
    Apply DOM prediction layer with xpath expressions.
    """
    # positive selection for clustering based on threshold
    threshold: float = 0.01
    rslt_df = dataframe[dataframe['BERT'] >= threshold]
    rslt_df.rename(columns={"A": "a", "B": "c"})
    rslt_df = rslt_df.drop(['BERT'], axis=1)

    # get html tree
    tree = html.fromstring(source.html)

    a_dom = []

    for link in rslt_df['link']:
        path = urlparse(link).path

        if path == "":
            continue

        a_dom = a_dom + tree.xpath('//a[contains(@href, "' + 
            path + '")]/..')

    dom_list = []

    for a in a_dom:

        if a is None:
            continue
        if a[0].tag != "a":
            continue

        dom_list.append(a)

    # build backpack (WSJTheme--headline--unZqjb45 	attribute=class 	count=1)
    bagpack = get_bagpack(dom_list)

    print(bagpack)

    # build attribute list (WSJTheme--headline--unZqjb45 	attribute=class 	count>1)
    liste_dom = get_attribute_list(dom_list, bagpack)

    ### CLUSTERING ###

    bag_of_words = []
    list_of_vectors = []

    # create bag of words
    for _, dom_df in liste_dom:
        for i in range(dom_df.count()['tag']):
            ref = dom_df['tag'][i] + "." + str(dom_df['parent'][i]) + "." + dom_df['attribute'][i] + "=" + \
                dom_df['value'][i]
            bag_of_words.append(ref)

    bag_of_words = set(bag_of_words)

    # create vectors
    for _, dom_df in liste_dom:
        ref = ""
        for i in range(dom_df.count()['tag']):
            ref += dom_df['tag'][i] + "." + str(dom_df['parent'][i]) + "." + dom_df['attribute'][i] + "=" + \
                dom_df['value'][i] + " "

        vector = []
        for w in bag_of_words:
            vector.append(ref.split().count(w))

        list_of_vectors.append(vector)

    ## PREDICTION ##
    X = np.array(list_of_vectors)
    db = DBSCAN(eps=0.5, min_samples=2, metric='cosine').fit(X)  # use cosine similarity to compute the distance

    db.fit(X)
    y_pred = db.fit_predict(X)

    ## CLUSTERS ##
    nb_cluster = y_pred.max() + 1
    print("Nb clusters: " + str(nb_cluster))

    threshold = 0.75  ## add to args
    list_simplified = []

    for i in range(0, nb_cluster):
        cl_vectors = X[y_pred == i]
        mean = cl_vectors.mean(axis=0)

        cl_simplified = np.array((mean > threshold) == True)
        list_simplified.append(cl_simplified)

    b_w = np.array(list(bag_of_words))

    for i in range(0, nb_cluster):
        print(b_w[list_simplified[i]])
        print("\n")

    # BUILD XPATH EXPRESSION
    xpath_list = to_xpath(nb_cluster, b_w, list_simplified)

    # FIND THE CORRECT LINKS
    _dom = []
    liste_href = []
    liste_dom = []
    ns = {"re": "http://exslt.org/regular-expressions"}

    for xpath in xpath_list:
        try:
            _dom = _dom + tree.xpath(xpath, namespaces=ns)
            print("expression validated: {}".format(xpath))
        except:
            print("Invalid expression: {}".format(xpath))


    for a_dom in _dom:
        href = a_dom.get('href')

        text = a_dom.text_content()

        if(len(text.split()) <= 4):
            continue  # skip
    
        if(href == None or href == ""):
            continue

        # Handle limit case :if href starts with //domain_name
        if(href[:2]) == '//':
            href = href[2:]
            href = href[href.find('/'):]

        if(href[0] == '/'):
            href = source.url + href

        _urlparse = urlparse(href)

        # Filter by extension
        find = re.search(r"\.(jpg|jpeg|svg|xml)$", _urlparse.path)

        if (find is not None):
            continue  # skip

        # Remove get parameters?
        liste_href.append(href)
        liste_dom.append(html.tostring(a_dom))

    result = pd.DataFrame({'URL': liste_href})

    true_name = list()
    for link in result['URL']:
        if not dataframe.loc[dataframe['link'] == link, 'title'].empty:
            title = dataframe.loc[dataframe['link'] == link, 'title'].iloc[0]
        else:
            title = ''
        true_name.append(title)

    result['title'] = true_name

    # merge DOM URL results with dframe 
    merged_df = pd.merge(
        dataframe[['link', 'title', 'BERT']].rename(columns={'link': 'URL'}), 
        result,
        on=['URL', 'title'], 
        how='left',
        indicator="predicted_class"
    )
    print("merged_df columns = ", list(merged_df))

    merged_df["predicted_class"] = np.where(merged_df["predicted_class"] == 'both', 1, 0)

    return merged_df