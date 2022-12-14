# -*- coding: utf-8 -*-
"""
File Name: DIHC_Downloader.py
Author: WWM Emran (Emran Ali)
Involvement: HumachLab (HML) & Deakin- Innovation in Healthcare (DIHC)
Email: wwm.emran@gmail.com, emran.ali@research.deakin.edu.au
Date: 5/07/2020 8:55 pm
"""


""" Nested file downloader from nested directories of a web directory

This script contains a class that allows some functions to download files from the web directory when a specific name 
of the web directory is provided. It automatically finds the links to the multilevel nested directories, sorts them 
accordingly and saves them in the corresponding nested directories. 
If the download is interrupted then next time with the same parameters it will start downloading from the file it was 
been interrupted, if the download directory contains the already downloaded files and folder structure. 
"""



""" Importing necessary modules
"""
# #%%
from tqdm import tqdm
import requests
# from requests.auth import HTTPDigestAuth
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup


# The base url and base directory will be provided later

class DIHC_Downloader:
    """ Downloader class that manages all the functionalities for downloading files

    This class contains all the properties requires to customize the properties of download processes. It also contains
    the functions used for directory traversal and byte movement (downloading).

    Properties
    -----------
    url_to_download : str
        Base URL of the web directory to download files from
    download_directory : str
        Download directory where the files will be stored
    Optional
    ---------
    username: str
        If the web directory needs authentication to access the contents
    password: str
        If the web directory needs authentication to access the contents
    file_types_to_download: list(str)
        List of the specific types of files to download
    file_types_not_to_download: list(str)
        List of the specific types of files to to be excluded to download
    folder_indicator: list(str)
        Special folder names containing special characters that are usually excluded but expected to be downloaded
    url_not_to_consider: list(str)
        Web directory may contain unnecessary links that can be considered as folders but are not and meant to be
        excluded during downloading
    is_need_html: bool
        If the web directory contains html file and instead of traversing thru the link to find folders, that html files
        are needed to be downloaded

    Methods
    --------
    __init()__
        Takes- Minimum two of the parameter values from above parameter list | Returns- Object of this class | Func-
        Creates an object with the corresponding parameter values assigned to it
    download()
        Takes- none | Returns- none | Func- Traverse thru the web directory to find the nested directories and their
        contents. Downloads them and sort accordingly in the local download directory.
    """


    # ### For initial settings
    # The target url to be downloaded
    url_to_download = ''
    # List of urls in a specific directory to be downloaded
    _url_list = []
    # Directory in which to save contents / Current directory by default
    download_directory = os.getcwd()
    # Username and password if basic authentication is needed
    username = ''
    _password = ''
    # List of file types(extension with dot; like- .txt/.avi) to be downloaded / Default all general file types
    _file_types_to_download = ['.']
    # List of file types(extension with dot; like- .txt/.avi) not to be downloaded / Default None
    _file_types_not_to_download = []
    # Some folder names might contain dots; to consider those as folder, a list could be provided
    _folder_indicator = ['../']
    # Pages might contain unnecessary urls; those can be added here for not considering those
    _url_not_to_consider = ['../', 'mailto:']
    # If anytime needed to download the HTML files without .html extension
    _is_need_html = False

    # ### For session url management
    _download_session = None

    # ###
    # ### Initialize url - optionally username & password if authenticatoin needed
    # ###
    def __init__(self, url_to_download, download_directory='./', username='', password='', file_types_to_download=[],
                 file_types_not_to_download=[], folder_indicator=[], url_not_to_consider=[], is_need_html=False):
        """Creates an object with the corresponding parameter values assigned to it

        Parameters
        ----------
        url_to_download : str
            Base URL of the web directory to download files from
        download_directory : str
            Download directory where the files will be stored
        Optional
        ---------
        username: str
            If the web directory needs authentication to access the contents
        password: str
            If the web directory needs authentication to access the contents
        file_types_to_download: list(str)
            List of the specific types of files to download
        file_types_not_to_download: list(str)
            List of the specific types of files to to be excluded to download
        folder_indicator: list(str)
            Special folder names containing special characters that are usually excluded but expected to be downloaded
        url_not_to_consider: list(str)
            Web directory may contain unnecessary links that can be considered as folders but are not and meant to be
            excluded during downloading
        is_need_html: bool
            If the web directory contains html file and instead of traversing thru the link to find folders, that html files
            are needed to be downloaded

        Returns
        -------
        object
            Object of this current class

        Examples
        --------
        Example-1:
            url = 'https://www.physionet.org/files/chbmit/1.0.0/'
            directory = './'
            unusual_folders = ['1.0.0']
            downloader = DIHC_Downloader(url, download_directory=directory, folder_indicator=unusual_folders)

        Example-2:
            url = 'https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_seizure/v1.5.1/'
            directory = './'
            unusual_folders = ['1.5.1', '../']
            unusual_url = ['/?']
            username = 'nedc_tuh_eeg'
            password = 'nedc_tuh_eeg'
            downloader = DIHC_Downloader(url, download_directory=directory, username=username, password=password, folder_indicator=unusual_folders, url_not_to_consider=unusual_url)
        """


        self.url_to_download = url_to_download
        self._download_session = requests.Session()
        self._url_list = [url_to_download]
        self.download_directory = os.path.abspath(download_directory)
        if not(os.path.exists(self.download_directory)):
            self.download_directory = os.path.abspath('./')
        self.download_directory = self.download_directory.replace('\\', '/')

        if username:
            self.username = username
        if password:
            self._password = password
        if file_types_to_download:
            self._file_types_to_download += file_types_to_download
        if file_types_not_to_download:
            self._file_types_not_to_download += file_types_not_to_download
        if folder_indicator:
            self._folder_indicator += folder_indicator
        if url_not_to_consider:
            self._url_not_to_consider += url_not_to_consider
        if is_need_html:
            self._is_need_html = True

    # ###
    # ### Download all the enlisted files and explore directories if any
    # ###
    def download(self):
        """Traverse thru the web directory to find the nested directories and their contents. Downloads them and sort
        accordingly in the local download directory.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Examples
        --------
            downloader.download()
        """


        print(
            '\n########################################\n      Download begins...      \n########################################\n')
        self._process_download(self._url_list)
        print(
            '\n########################################\nFinished with all downloads...\n########################################\n')
        return



    # ######################################## Private methods zone ########################################
    # ###
    # ### Download all the enlisted files and explore directories if any
    # ###
    def _process_download(self, url_list):
        length_of_the_list = len(url_list)

        while (length_of_the_list > 0):
            specific_url = url_list[0]

            content_type = self._find_content_type_of_the_url(specific_url)

            # ### Checks for file/directory, ==1 means file
            if (content_type == 1 or content_type == 3):
                print('file...', specific_url)

                if (content_type == 1):
                    parser = urlparse(specific_url)
                    filename = os.path.basename(parser.path)
                    if filename.endswith('/'):
                        filename = filename[:-1]
                    if filename.startswith('/'):
                        filename = filename[1:]
                    filename = self.download_directory + '/' + filename

                    is_downloaded = self._download_specific_file(specific_url)

                    if (is_downloaded == 1):
                        print('### Download successful %s' % specific_url)
                        if os.path.exists((filename + '.tmp')):
                            os.rename((filename + '.tmp'), filename)
                    elif (is_downloaded == 2):
                        print('$$$ Already downloaded %s' % specific_url)
                    else:
                        print('@@@ Problem downloading %s' % specific_url)
                        # if os.path.exists((filename+'.tmp')):
                        #    os.remove((filename+'.tmp'))

                url_list.remove(specific_url)
                length_of_the_list -= 1
                # print('==>', len(url_list), length_of_the_list)

                if len(url_list) == 0:
                    res = self.download_directory.rfind('/', 0, len(self.download_directory))
                    self.download_directory = self.download_directory[:res]
                    print('$$$ Finished downloading directory--- ', self.download_directory)
                    return
                else:
                    continue
            else:
                print('directory...', specific_url)
                temp_url = self._explore_and_show_all_files_and_directories(specific_url)
                url_list.pop(0)
                length_of_the_list = len(url_list)

                # specific_url.strip(' /')
                if specific_url.endswith('/'):
                    specific_url = specific_url[:-1]
                loc = (specific_url.split('/')[-1])
                if loc:
                    self.download_directory += '/' + loc

                if not os.path.exists(self.download_directory):
                    os.mkdir(self.download_directory)

                self._process_download(temp_url)

        res = self.download_directory.rfind('/', 0, len(self.download_directory))
        self.download_directory = self.download_directory[:res]

    # ###
    # ### Finds the type of the url is file or directory, =0 folder, =1 file & =3 skip it
    # ###
    def _find_content_type_of_the_url(self, content_url):
        is_the_url_a_file = 0
        req = None

        urlparser = urlparse(content_url)
        filename = os.path.basename(urlparser.path)
        if filename.endswith('/'):
            filename = filename[:-1]
        if filename.startswith('/'):
            filename = filename[1:]
        # filename.strip(' /')
        # print(content_url, filename)

        if (not filename):
            pass

        elif (any(x in filename for x in self._folder_indicator)):
            pass

        elif (any(x in filename for x in self._file_types_not_to_download)):
            is_the_url_a_file = 2
        else:
            if (len(self._file_types_to_download) == 1):
                is_the_url_a_file = 1
            elif (len(self._file_types_to_download) > 1 and any(x in filename for x in self._file_types_to_download[1:])):
                is_the_url_a_file = 1
            else:
                pass

        try:
            if not (self.username and self._password):
                req = self._download_session.head(content_url, stream=True)
            else:
                req = self._download_session.head(content_url, auth=(self.username, self._password), stream=True)

            # print('Web url:', req.status_code, content_url)
            if req.status_code == 200:
                try:
                    if (req.headers['Content-Encoding'].find('gzip') != -1 and req.headers['Content-Type'].find(
                            'html') != -1):
                        # print('-------> possibly folder')
                        if (self._is_need_html or filename.find('html') != -1 or filename.find('htm') != -1):
                            # print('-------> thought as folder but is file')
                            is_the_url_a_file = 1
                    else:
                        # print('-------> file')
                        is_the_url_a_file = 1
                        # content_type = (req.headers['Content-Type'].split(';'))[0]
                        # if (content_type.find('plain') != -1 or content_type.find('application') != -1):
                        #    is_the_url_a_file = 1
                except:
                    print('File type in server not found.')

            else:
                print('Status code {}: Something went wrong getting header information.'.format(req.status_code, req))
        except:
            print('Sorry, something went wrong getting header information.')

        if req:
            req.close()

        return (is_the_url_a_file)

    # ###
    # ### Explore and display all files and directories in specific web location
    # ###
    def _explore_and_show_all_files_and_directories(self, web_url):
        new_url_list = []
        req = None

        try:
            if (not self.username):
                req = self._download_session.get(web_url, stream=True)
            else:
                req = self._download_session.get(web_url, auth=(self.username, self._password), stream=True)

            if req.status_code == 200:
                web_page = req.text

                if not web_url.endswith('/'):
                    web_url += '/'

                soup = BeautifulSoup(web_page, 'html.parser')
                urls_from_webpage = [web_url + node.get('href') for node in soup.find_all('a')]

                for node in urls_from_webpage:
                    # Test for text files only
                    # if (node.find('.txt')>0 or (node.endswith('/') and not node.endswith('../'))):
                    if (node.count('//') == 1 and not any(x in node for x in self._url_not_to_consider)):
                        new_url_list.append(node)
            else:
                print('Status code {}: Something went wrong during url request.'.format(req.status_code, req))

        except:
            print('Sorry, something went wrong during url request.')

        if req:
            req.close()

        return new_url_list

    # ###
    # ### Download a specific file with url with its progress report =1 complete, =2 already downloaded, =0 problem downloading
    # ###
    def _download_specific_file(self, file_url):
        is_download_complete = 0
        req = None

        parser = urlparse(file_url)
        filename = os.path.basename(parser.path)
        if filename.endswith('/'):
            filename = filename[:-1]
        if filename.startswith('/'):
            filename = filename[1:]
        # filename = filename.strip(' /')
        filename2 = self.download_directory + '/' + filename

        try:
            if (not self.username):
                req2 = self._download_session.head(file_url, stream=True)
            else:
                req2 = self._download_session.head(file_url, auth=(self.username, self._password), stream=True)

            if req2.status_code == 200:
                chunk_size = 1024  # in bytes
                total_size = 0

                # ### Resuming file download
                # accept_ranges = None
                resume_header = None
                resume_byte_pos = 0
                try:
                    # accept_ranges = req2.headers['Accept-Ranges']
                    if (os.path.exists(filename2 + '.tmp')):
                        resume_byte_pos = os.path.getsize(filename2 + '.tmp')
                        resume_header = {'Range': 'bytes={}-'.format(resume_byte_pos)}
                        # print('&&&& ', resume_byte_pos, resume_header)
                except:
                    print('Sorry, file download is not resumable in this server.')

                try:
                    total_size = int(req2.headers['content-length'])
                except:
                    print('File size in server not found.')
                    total_size = 0

                if (not self.username):
                    req = self._download_session.get(file_url, headers=resume_header, stream=True)
                    # req = self._download_session.get(file_url, stream=True)
                else:
                    req = self._download_session.get(file_url, auth=(self.username, self._password),
                                                     headers=resume_header, stream=True)
                    # req = self._download_session.get(file_url, auth=(self.username, self._password), stream=True)

                tqdm_description = 'Downloading \"' + filename + '\"'
                tqdm_task = tqdm(iterable=req.iter_content(chunk_size=chunk_size), total=total_size / chunk_size,
                                 unit='KB', desc=tqdm_description)

                filename = filename2  # self.download_directory+'/'+filename
                # print('$$$-> ', filename, ' ', total_size, ' ', file_url)

                if (os.path.exists(filename)):
                    is_download_complete = 2
                    tqdm_task.update(total_size / chunk_size)
                    # print(filename, ' ', total_size, " ", (os.stat(filename).st_size))
                    # print('Already downloaded!')
                elif ((not os.path.exists(filename) and not os.path.exists(filename + '.tmp')) or (
                        os.path.exists(filename + '.tmp'))):
                    try:
                        # print('Downloading...')
                        file_writing_mode = 'ab'
                        # if resume_byte_pos==0:
                        #    file_writing_mode = 'wb'
                        print('&&&&&', resume_byte_pos, filename + '.tmp')
                        current_data_byte = 0

                        with open((filename + '.tmp'), file_writing_mode) as f:
                            for data in tqdm_task:
                                if current_data_byte >= resume_byte_pos:
                                    f.write(data)
                                current_data_byte += len(data)

                        # tqdm_task.update(total_size/chunk_size)
                        is_download_complete = 1
                    except:
                        print('Sorry, something went wrong internally downloading file data.')
                        is_download_complete = 0

                else:
                    print('Sorry, can not download file.')
                    is_download_complete = 0
            else:
                print('Status code {}: Something went wrong downloading file.'.format(req.status_code, req))
                is_download_complete = 0;

        except:
            print('Sorry, something went wrong downloading file.')
            is_download_complete = 0;
            # if os.path.exists((filename+'.tmp')):
            #    os.remove((filename+'.tmp'))

        if req:
            req.close()
        return (is_download_complete)



