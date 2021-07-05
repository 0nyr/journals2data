if(
    self.config.params["VERBOSE"].value == 
    utils.enums.VerboseLevel.COLOR
):
    console.println_ctrl_sequence(
        "text",
        console.ANSICtrlSequence.PASSED
    )