import requests
import webbrowser

s = requests.session()  # Start new session to keep track of everything
clientID="743e391dfa9a4581beb6266c2fbe408a"  # ClientID for parameter
parameters={'client_id':clientID,'response_type':'token','redirect_uri':'http://example.com','scope':'user-top-read','show_dialog':'true'}  # Parameters to get authorization code
BaseURL='https://accounts.spotify.com/authorize'  # URL to pass for authorization code
r=s.get(BaseURL, params=parameters)  # Get request to get authorization code URL
# print(r.url)  # Uncomment this and comment the following line to have the URL printing in the console to be used, instead of a webpage to open automatically
webbrowser.open(r.url)  # Open URL from get request to allow user to log in
returnURL=str(input("Enter URL of redirected page:\n"))  # Get URL containing access token from user
splitURL=returnURL.split('&')  # Split URL input by '&' sign to limit down to access token
accessTokenList=splitURL[0].split('#access_token=')  # Continue splitting URL down to access token and excess information
accessToken=accessTokenList[1]  # Splitting URL down to get access token by itself
header={'Authorization':'Bearer '+accessToken, "Content-Type":"application/json"}  # Header for get requests, as they require access token
r=s.get("https://api.spotify.com/v1/me",headers=header)
topTracks=""

limit=20  # Limit of top songs to get (Change this number to print different amount of top tracks)

if(r.json()["display_name"]=="TestAccount"):  # Test account needs medium term
    r=s.get("https://api.spotify.com/v1/me/top/tracks",headers=header,params={"limit":limit,"time_range":"long_term"})  # Get request for top songs of user
    topTracks=r.json()  # Top songs info from get request
else:  # Not test account
    r=s.get("https://api.spotify.com/v1/me/top/tracks",headers=header,params={"limit":limit,"time_range":"short_term"})  # Get request for top songs of user
    topTracks=r.json()  # Top songs info from get request
x=0
while x<limit:  # While loop to go through each top track
    topTrackName=topTracks['items'][x]['name']  # Name of top song(s)
    trackID=topTracks['items'][x]['id']  # ID of top track for recommendation seed
    artistID=topTracks['items'][x]['artists'][0]['id']  # ID of track's artist for recommendation seed
    r=s.get("https://api.spotify.com/v1/artists/"+artistID,headers=header)  # Get request for top artist information
    artistInfo=r.json()  # Info on artist from get request
    Genre=artistInfo['genres']  # Genre(s) of top track's artist

    recoLimit=5  # *** Number of songs to be recommended (Change this to choose number of songs to be recommended per track) ***
    
    r=s.get("https://api.spotify.com/v1/recommendations",headers=header,params={"limit":recoLimit,'seed_artists':artistID,'seed_tracks':trackID,'seed_genre':Genre})  # Get request for recommendation songs using seeds from top tracks 
    print("\nTop Track: "+topTrackName+" - Recommended Songs:")  # Printing top track for user
    y=0
    while y<recoLimit:  # While loop to print recommended tracks+respective artist(s) for each top song
        print("Track: "+r.json()['tracks'][y]['name'],end="")  # Printing recommended track
        if(len(r.json()['tracks'][y]['artists'])>1):  # If statement for is the song has more than one artist
            print(" ----- Artist(s): ",end="")  # Start of recommended artists print, using ending definition to print on same line
            z=0
            while z<len(r.json()['tracks'][y]['artists']):  # While loop to go through each artist from recommended track
                if(z==0):  # If first artist
                    print(r.json()['tracks'][y]['artists'][z]['name'],end="")  # Print with no comma separator, and ending definition to continue the print on the same line
                elif(z==len(r.json()['tracks'][y]['artists'])-1):  # If last artist
                    print(", "+r.json()['tracks'][y]['artists'][z]['name'])  # Print with comma separator and no ending definition to stop printing on same line
                else:  # Any other line (Not first nor last line)
                    print(", "+r.json()['tracks'][y]['artists'][z]['name'],end="")  # Print with comma separator and ending definition to continue print on same line
                z+=1
        else:  # If only one artist for recommended track
            print(" ----- Artist(s): "+r.json()['tracks'][y]['artists'][0]['name'])  # Print recommended track's artist with no ending defintion to print to next line  
        y+=1    
    x+=1
s.cookies.clear()  # Clear cookies of session to kill current access token for new request
