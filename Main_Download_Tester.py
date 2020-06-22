
### Test Download module
import os
from HumachLab_Downloader import HumachLab_Downloader

# ### CHB-MIT EEG Dataset
# url = 'https://www.physionet.org/files/chbmit/1.0.0/'
# #directory = os.path.abspath('./../CHB_MIT_EEG_Dataset')
# directory = os.path.abspath('./')
# unusual_folders = ['1.0.0']
#
# downloader = HumachLab_Downloader(url, download_directory=directory, folder_indicator=unusual_folders)


### Nureca-TUH (Temple University Hospital) Dataset
url = 'https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_seizure/v1.5.1/'
#url = 'https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_seizure/v1.5.1/_DOCS/parameter_files/'
#directory = os.path.abspath('./../TUH_EEG_Dataset')
directory = os.path.abspath('./')
unusual_folders = ['1.5.1', '../']
unusual_url = ['/?']
username = 'nedc_tuh_eeg'
password = 'nedc_tuh_eeg'

downloader = HumachLab_Downloader(url, download_directory=directory, username=username, password=password, folder_indicator=unusual_folders, url_not_to_consider=unusual_url)

#print(downloader.download_directory)
downloader.download()


