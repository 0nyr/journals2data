"""
This type stub file was generated by pyright.
"""

VIDEOS_TAGS = ...
VIDEO_PROVIDERS = ...
class VideoExtractor:
    """Extracts a list of video from Article top node
    """
    def __init__(self, config, top_node) -> None:
        ...
    
    def get_embed_code(self, node): # -> str:
        ...
    
    def get_embed_type(self, node):
        ...
    
    def get_width(self, node):
        ...
    
    def get_height(self, node):
        ...
    
    def get_src(self, node):
        ...
    
    def get_provider(self, src): # -> str | None:
        ...
    
    def get_video(self, node): # -> Video:
        """Create a video object from a video embed
        """
        ...
    
    def get_iframe_tag(self, node): # -> Video:
        ...
    
    def get_video_tag(self, node): # -> Video:
        """Extract html video tags
        """
        ...
    
    def get_embed_tag(self, node): # -> Video | None:
        ...
    
    def get_object_tag(self, node): # -> Video | None:
        ...
    
    def get_videos(self): # -> list[Unknown]:
        ...
    


