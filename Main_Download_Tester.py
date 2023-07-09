# -*- coding: utf-8 -*-
"""
File Name: Main_Download_Test.py
Author: WWM Emran (Emran Ali)
Involvement: HumachLab (HML) & Deakin- Innovation in Healthcare (DIHC)
Email: wwm.emran@gmail.com, emran.ali@research.deakin.edu.au
Date: 5/07/2020 8:55 pm
"""


""" DIHC Downloader class test script

This script contains two example scenarios of using DIHC_Downloader class to download the contents from the web 
directory. One of the web directories requires authentication to access its contents. 
"""



""" Importing necessary modules
"""
# #%%
# ### Test Download module
from DIHC_Downloader import DIHC_Downloader


""" Test parameter setup for normal web directory
"""
# #%%
# ### CHB-MIT Epilepsy EEG Dataset
# url = 'https://www.physionet.org/files/chbmit/1.0.0/'
# #directory = './../CHB_MIT_EEG_Dataset'
# directory = './'
# unusual_folders = ['1.0.0']
#
# downloader = DIHC_Downloader(url, download_directory=directory, folder_indicator=unusual_folders)


# """ Test parameter setup for normal web directory - 2
# """
# #%%
# ### CAP Sleep EEG Dataset
# url = 'https://physionet.org/files/capslpdb/1.0.0/'
# #directory = './../CHB_MIT_EEG_Dataset'
# directory = './'
# unusual_folders = ['1.0.0']
#
# downloader = DIHC_Downloader(url, download_directory=directory, folder_indicator=unusual_folders)


# """ Test parameter setup for normal web directory - 3
# """
# #%%
# ### Sleep edfx (EDF-extended) EEG Dataset
# url = 'https://physionet.org/files/sleep-edfx/1.0.0/'
# #directory = './../CHB_MIT_EEG_Dataset'
# directory = './'
# unusual_folders = ['1.0.0']
#
# downloader = DIHC_Downloader(url, download_directory=directory, folder_indicator=unusual_folders)


""" Test parameter setup for normal web directory - 4
"""
#%%
### Sleep edf (EDF) EEG Dataset
url = 'https://physionet.org/files/sleep-edfx/1.0.0/'
#directory = './../CHB_MIT_EEG_Dataset'
directory = './'
unusual_folders = ['1.0.0']

downloader = DIHC_Downloader(url, download_directory=directory, folder_indicator=unusual_folders)



""" Test parameter setup with web directory that requires authentication credentials
"""
# #%%
# ### Nureca-TUH (Temple University Hospital) Dataset
# url = 'https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_seizure/v1.5.1/'
# #url = 'https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_seizure/v1.5.1/_DOCS/parameter_files/'
# #directory = './../TUH_EEG_Dataset'
# directory = './'
# unusual_folders = ['1.5.1', '../']
# unusual_url = ['/?']
# username = 'nedc_tuh_eeg'
# password = 'nedc_tuh_eeg'
#
# downloader = DIHC_Downloader(url, download_directory=directory, username=username, password=password, folder_indicator=unusual_folders, url_not_to_consider=unusual_url)



""" Strat downloading process
"""
# #%%
#print(downloader.__dict__)
downloader.download()

# #%%

