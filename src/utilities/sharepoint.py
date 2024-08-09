import logging
import os
from scp import SCPClient 
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File 
from os.path import abspath

class SharePoint:
    """
    Class for SharePoint File functions.
    """

    logger = logging.getLogger(os.getenv('LOG_ENV'))

    def __init__(self, sharepoint_base_url, client_id, client_secret):
        """Initialize the logger for SharePoint"""
        self.auth = AuthenticationContext(sharepoint_base_url)
        self.auth.acquire_token_for_app(client_id=client_id, client_secret=client_secret)
        self.ctx = ClientContext(sharepoint_base_url, self.auth)

        try:
            web = self.ctx.web
            self.ctx.load(web)
            self.ctx.execute_query()
            SharePoint.logger.info(f'Connected to SharePoint: {web.properties["Title"]}')
        except Exception as e:
            SharePoint.logger.error(f'Error connecting to SharePoint: {e}')

    def pull(self, folder_in_sharepoint, local_directory=None):
        """
        Pulls files from a SharePoint folder to a local directory.

        Args:
            folder_in_sharepoint (str): Relative URL of the SharePoint folder.
            local_directory (str): Optional. Directory path where files will be saved locally.
                                   If not provided, files will be saved in the current working directory.
        """
        try:
            # Getting folder details
            folder = self.ctx.web.get_folder_by_server_relative_url(folder_in_sharepoint)
            fold_names = []
            sub_folders = folder.files
            self.ctx.load(sub_folders)
            self.ctx.execute_query()
            for s_folder in sub_folders:
                fold_names.append(s_folder.properties["Name"])

            # Printing list of files from SharePoint folder
            SharePoint.logger.info(f'This is the list of files: {fold_names}')

            # Determine save directory
            if local_directory:
                save_directory = os.path.abspath(local_directory)
            else:
                save_directory = os.getcwd()

            # Loop to save all files in the directory
            # Reading File from SharePoint Folder
            for file in fold_names:
                sharepoint_file = folder_in_sharepoint + file
                file_response = File.open_binary(self.ctx, sharepoint_file)

                # Saving file to local_directory
                local_file_path = os.path.join(save_directory, file)
                with open(local_file_path, 'wb') as output_file:
                    output_file.write(file_response.content)
                    SharePoint.logger.info(f'File saved locally: {abspath(output_file.name)}')

        except Exception as e:
            SharePoint.logger.error(f'Error pulling files from SharePoint: {e}')

    def push(self, file_path, folder_in_sharepoint):
        """
        Uploads a file to a SharePoint library.
        
        Args:
            file_path (str): The path to the file to upload.
            folder_in_sharepoint (str): Relative URL of the SharePoint folder to upload to.
            
        Returns:
            str: The URL of the uploaded file.
        """
        try:
            file_name = os.path.basename(file_path)

            with open(file_path, 'rb') as content_file:
                file_content = content_file.read()

            library_root = self.ctx.web.get_folder_by_server_relative_url(folder_in_sharepoint)

            target_file = library_root.upload_file(file_name, file_content).execute_query()
            uploaded_url = target_file.serverRelativeUrl
            SharePoint.logger.info(f'File has been uploaded to URL: {uploaded_url}')

            return uploaded_url

        except Exception as e:
            SharePoint.logger.error(f'Error uploading file to SharePoint: {e}')

    def disconnect(self):
        self.ctx.dispose()
        SharePoint.logger.info('Disconnected from SharePoint')