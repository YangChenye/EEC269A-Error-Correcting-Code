# Copyright (c) 2023 Name

import logging

from Source import source
from Channel import channel
from Destination import destination


# Configure the logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger in the main module
logger = logging.getLogger(__name__)




def error_correct():
    """
        Description of function

            @type  variable: type
            @param variable: description

            @rtype:   return typr
            @return:  description
    """
    data_src = source.Source()
    data_chl = channel.Channel()
    data_dest = destination.Destination()
    pass




if __name__ == '__main__':
    error_correct()