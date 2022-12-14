from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from dotenv import load_dotenv


# This is the function to download a zip file of all the spotify playlists in a given account.
# It takes advantage of selenium to run exportify.
def playlistdownloader(downloadsPath):
    try:
        os.environ['MOZ_HEADLESS'] = '1'
        load_dotenv()
        USERNAME = os.getenv("SPOTIFY_USERNAME")
        PASSWORD = os.getenv("SPOTIFY_PASSWORD")
        # Open web browser and clear downloads folder of zipped file (important for checks later on)
        driver = webdriver.Firefox()
        action = ActionChains(driver)
        zippedFile = "spotify_playlists.zip"

        # Maximise window and navigate to exportify and click login
        driver.get("https://watsonbox.github.io/exportify/")
        exportifyLogin = driver.find_element(By.ID, "loginButton")
        action.move_to_element(exportifyLogin).click(exportifyLogin).perform()
        time.sleep(5)
        # Login to spotify
        spotifyUsername = driver.find_element(By.ID, "login-username")
        spotifyPassword = driver.find_element(By.ID, "login-password")
        spotifyLoginButton = driver.find_element(By.ID, "login-button")
        spotifyUsername.send_keys(USERNAME)
        spotifyPassword.send_keys(PASSWORD)
        action.move_to_element(spotifyLoginButton).click(spotifyLoginButton).perform()
        time.sleep(5)
        # TAB to appropriate button and press enter (this exports all users playlists)
        i = 8
        print("\n\nWaiting for extraction of playlists and subsequent zip file download")
        exportAll = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/table/thead/tr/th[7]/button")
        action.move_to_element(exportAll).click(exportAll).perform()

        # while i > 0:
        #     action.send_keys(Keys.TAB).perform()
        #     i -= 1
        #     time.sleep(1)
        # action.send_keys(Keys.ENTER).perform()
        print("\nStarting download of playlists\n")
        # Check to close browser only after the file exists and has had a few seconds to download.
        # On a slow connection this may be an issue
        try:
            os.remove(downloadsPath + zippedFile)
        except:
            print("")
        fileExists = False
        counter = 0
        while not fileExists:
            fileExists = os.path.exists(downloadsPath + zippedFile)
            time.sleep(1)
            counter += 1
            if counter > 1000:
                fileExists = True


        # Check if zip file downlaoded after timeout
        if os.path.exists(downloadsPath+zippedFile):
            print("Playlists downloaded\n\n")
        # If zip file not found, check for old downloaded playlist data, if not found exit
        elif not (os.path.exists(downloadsPath + zippedFile)):
            print("Checking for old playlist information\n\n")
            for root, dirs, files in os.walk(downloadsPath):
                # print(dirs)
                try:
                    if dirs[0] is not None:
                        for directory in dirs:
                            # print("Directory = " + directory)
                            if directory.contains("playlists"):
                                print("Playlist download timed out. Continuing on old playlist information")
                except:
                    if files is not None:
                        print("Error downloading, using old information.")

        # Close window
        driver.close()

    except:
        print("Error downloading, moving on with script")
