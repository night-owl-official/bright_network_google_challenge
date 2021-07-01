"""A video player class."""

import random
from .video_library import VideoLibrary
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()

        self._video_playing = self._video_library.get_video(None)
        self._video_paused = self._video_library.get_video(None)

        self._playlists = []
        self._flagged_videos = []


    def get_tags_string(self, video):
        # Build the tag string
        # We could unpack the tuple but this way we can have as many tags as we want
        ts = '['

        for tag in video.tags:
            ts += f"{tag} "

        ts = ts.strip()
        ts += ']'

        return ts

    def display_video_search_results(self, found_vids, search_criterion):
        # No video was found meeting the search criteria
        if len(found_vids) == 0:
            print("No search results for " + search_criterion)
            return False

        # Order the found videos list by title
        found_vids.sort(key = lambda vd: vd.title)

        # Some video/s was/were found, display it/them
        print("Here are the results for " + search_criterion + ':')
        for i in range(0, len(found_vids)):
            print('\t' + f"{i + 1})", end = ' ')
            print(f"{found_vids[i].title} ({found_vids[i].video_id}) {self.get_tags_string(found_vids[i])}")

        return True

    def ask_user_video_to_play(self, found_vids):
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        choice = input()

        # Make sure the input is a number
        if choice.isdigit():
            # Convert it to an integer
            choice = int(choice)
            # The number needs to be within the boundary of the found videos list
            if choice <= len(found_vids) and choice > 0:
                self.play_video(found_vids[choice - 1].video_id)


    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""

        # Get all the videos from the library
        videos = self._video_library.get_all_videos()

        # Sort videos by their title
        videos.sort(key = lambda vid: vid.title)

        print("Here's a list of all available videos:")
        for video in videos:
            tag_string = self.get_tags_string(video)

            # Add an indicator for flagged videos
            for vid in self._flagged_videos:
                if vid["video"] == video:
                    tag_string += f" - FLAGGED (reason: {vid['flag_reason']})"
                    break

            print('\t' + f"{video.title} ({video.video_id}) {tag_string}")

            # Reset the tag string for the next video
            tag_string = ""


    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

        video_to_play = self._video_library.get_video(video_id)

        # Video doesn't exist
        if not video_to_play:
            print("Cannot play video: Video does not exist")
            return

        # Stop currently playing video if there is one
        if self._video_playing:
            self.stop_video()
            # Forget about any paused video
            self._video_paused = self._video_library.get_video(None)

        # Cannot play flagged videos
        for flagged_video in self._flagged_videos:
            if flagged_video["video"].video_id == video_id:
                print("Cannot play video: Video is currently flagged " + f"(reason: {flagged_video['flag_reason']})")
                return

        # Set the currently playing video
        self._video_playing = video_to_play
        print("Playing video: " + video_to_play.title)

    def stop_video(self):
        """Stops the current video."""

        # No video is currently playing
        if not self._video_playing:
            print("Cannot stop video: No video is currently playing")
            return

        # Stop the playing video
        print("Stopping video: " + self._video_playing.title)
        self._video_playing = self._video_library.get_video(None)

         # Forget about any paused video
        self._video_paused = self._video_library.get_video(None)

    def play_random_video(self):
        """Plays a random video from the video library."""

        # Add only the non flagged videos to the list
        non_flagged_videos = []
        flagged_video_found = False
        for vid in self._video_library.get_all_videos():
            for fvid in self._flagged_videos:
                if fvid["video"] == vid:
                    flagged_video_found = True
            
            # If a flagged video was found in this iteration
            # don't add it to the list
            if not flagged_video_found:
                non_flagged_videos.append(vid)

            # Reset the flag for the next iteration
            flagged_video_found = False

        # No videos are available or they're all flagged
        if len(non_flagged_videos) == 0:
            print("No videos available")
            return

        # Play random video
        self.play_video(non_flagged_videos[random.randint(0, len(non_flagged_videos) - 1)].video_id)

    def pause_video(self):
        """Pauses the current video."""

        # No video is playing
        if not self._video_playing:
            print("Cannot pause video: No video is currently playing")
            return

        # Video is already paused
        if self._video_paused:
            print("Video already paused: " + self._video_paused.title)
            return
        
        # Pause the video
        self._video_paused = self._video_playing
        print("Pausing video: " + self._video_playing.title)

    def continue_video(self):
        """Resumes playing the current video."""

        # No video is playing
        if not self._video_playing:
            print("Cannot continue video: No video is currently playing")
            return

        # No video is paused
        if not self._video_paused:
            print("Cannot continue video: Video is not paused")
            return

        # Video is paused, continue playing it
        print("Continuing video: " + self._video_playing.title)

        # Forget about any paused video
        self._video_paused = self._video_library.get_video(None)

    def show_playing(self):
        """Displays video currently playing."""

        # No video is playing
        if not self._video_playing:
            print("No video is currently playing")
            return

        # Construct the string to display for playing video
        playing_string = f"{self._video_playing.title} ({self._video_playing.video_id}) {self.get_tags_string(self._video_playing)}"

        # Add an extra string to the playing string when a video is paused
        playing_string += " - PAUSED" if self._video_paused else ""

        # Display playing video
        print("Currently playing: " + playing_string)

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        # Playlist already exists
        for plist in self._playlists:
            if playlist_name.lower() == plist.name.lower():
                print("Cannot create playlist: A playlist with the same name already exists")
                return

        # Playlist is new
        self._playlists.append(Playlist(playlist_name, []))
        print("Successfully created new playlist: " + playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        
        for plist in self._playlists:
            video_to_add = self._video_library.get_video(video_id)

            # Playlist found but video does not exist
            if playlist_name.lower() == plist.name.lower() and not video_to_add:
                print("Cannot add video to " + playlist_name + ": Video does not exist")
                return
            elif playlist_name.lower() == plist.name.lower() and video_to_add:
                # Cannot add flagged videos to the playlist
                for flagged_video in self._flagged_videos:
                    if flagged_video["video"].video_id == video_id:
                        print("Cannot add video to " + playlist_name + ": Video is currently flagged " + f"(reason: {flagged_video['flag_reason']})")
                        return

                # Video is already in the playlist
                for added_video in plist.videos:
                    if added_video.video_id == video_to_add.video_id:
                        print("Cannot add video to " + playlist_name + ": Video already added")
                        return

                # Video wasn't in the playlist
                plist.videos.append(video_to_add)
                print("Added video to " + playlist_name + ": " + video_to_add.title)
                return

        
        # Playlist not found
        print("Cannot add video to " + playlist_name + ": Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""

        # Playlist is empty
        if len(self._playlists) == 0:
            print("No playlists exist yet")
            return

        # Sort the playlists by name
        self._playlists.sort(key = lambda pl: pl.name)

        # Show all available playlists
        print("Showing all playlists:")
        for plist in self._playlists:
            print('\t' + plist.name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        for plist in self._playlists:
            # Playlist found
            if playlist_name.lower() == plist.name.lower():
                print("Showing playlist: " + playlist_name)

                # No videos in the playlist
                if len(plist.videos) == 0:
                    print("\tNo videos here yet")
                    return
                
                # Display all the videos in the playlist
                for pl_video in plist.videos:
                    # Construct a string to append to flagged videos if
                    # there is any, otherwise leave it blank
                    flag_string = ""
                    for fvid in self._flagged_videos:
                        if fvid["video"] == pl_video:
                            flag_string = " - FLAGGED " + f"(reason: {fvid['flag_reason']})"

                    print('\t' + f"{pl_video.title} ({pl_video.video_id}) {self.get_tags_string(pl_video)}" + flag_string)

                return
        
        # Playlist not found
        print("Cannot show playlist " + playlist_name + ": Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        for plist in self._playlists:
            video_to_remove = self._video_library.get_video(video_id)

            # Playlist found but video does not exist
            if playlist_name.lower() == plist.name.lower() and not video_to_remove:
                print("Cannot remove video from " + playlist_name + ": Video does not exist")
                return
            elif playlist_name.lower() == plist.name.lower() and video_to_remove:
                # Video is in the playlist and can be removed
                for pl_video in plist.videos:
                    if pl_video.video_id == video_to_remove.video_id:
                        plist.videos.remove(pl_video)
                        print("Removed video from " + playlist_name + ": " + video_to_remove.title)
                        return
                
                # Video wasn't in the playlist
                print("Cannot remove video from " + playlist_name + ": Video is not in playlist")
                return

        
        # Playlist not found
        print("Cannot remove video from " + playlist_name + ": Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        for plist in self._playlists:
            # Playlist found
            if playlist_name.lower() == plist.name.lower():
                # There are videos in the playlist, remove them all
                if len(plist.videos) > 0:
                    plist.videos.clear()
                    print("Successfully removed all videos from " + playlist_name)
                    return

                # Playlist is empty
                print("Cannot clear playlist " + playlist_name + ": Playlist is empty")
                return

        
        # Playlist not found
        print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        for plist in self._playlists:
            # Playlist found, delete it
            if playlist_name.lower() == plist.name.lower():
                self._playlists.remove(plist)
                print("Deleted playlist: " + playlist_name)
                return

        # Playlist does not exist
        print("Cannot delete playlist " + playlist_name + ": Playlist does not exist")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """

        all_videos = self._video_library.get_all_videos()
        videos_with_search_term = []

        # Look for the search term in all the videos
        for vid in all_videos:
            is_flagged = False

            # Search term found in a video title
            if search_term.lower() in vid.title.lower():
                # Only non flagged videos can be searched
                for fvid in self._flagged_videos:
                    if fvid["video"] == vid:
                        is_flagged = True

                if not is_flagged:
                    videos_with_search_term.append(vid)

        # Display search results and only ask the user to select a video to play
        # if the search was successful
        if self.display_video_search_results(videos_with_search_term, search_term):
            # Ask the user if they want to play any of the shown videos
            self.ask_user_video_to_play(videos_with_search_term)


    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """

        all_videos = self._video_library.get_all_videos()
        videos_with_tag = []

        # Look for the tag in all the videos
        for vid in all_videos:
            is_flagged = False

            # Only non flagged videos can be searched
            for fvid in self._flagged_videos:
                if fvid["video"] == vid:
                    is_flagged = True

            # Tag found for a video
            if not is_flagged:
                for tag in vid.tags:
                    if video_tag.lower() == tag.lower():
                        videos_with_tag.append(vid)

        # Display search results and only ask the user to select a video to play
        # if the search was successful
        if self.display_video_search_results(videos_with_tag, video_tag):
            # Ask the user if they want to play any of the shown videos
            self.ask_user_video_to_play(videos_with_tag)

    def flag_video(self, video_id, flag_reason = "Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        
        for vid in self._video_library.get_all_videos():
            # Video exists
            if video_id == vid.video_id:
                # Video is already flagged
                for f_vid in self._flagged_videos:
                    if f_vid["video"].video_id == video_id:
                        print("Cannot flag video: Video is already flagged")
                        return

                # Stop the video if it's playing or it's paused
                if (self._video_playing and self._video_playing == vid) or (self._video_paused and self._video_paused == vid):
                    self.stop_video()

                # Video exists but isn't flagged, flag it
                self._flagged_videos.append({"video": vid, "flag_reason": flag_reason})
                print("Successfully flagged video: " + vid.title + f" (reason: {flag_reason})")
                return

        # Video does not exist
        print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """

        for vid in self._video_library.get_all_videos():
            # Video exists
            if video_id == vid.video_id:
                # Video was flagged, unflag it
                for f_vid in self._flagged_videos:
                    if f_vid["video"].video_id == video_id:
                        self._flagged_videos.remove(f_vid)
                        print("Successfully removed flag from video: " + vid.title)
                        return


                # Video exists but isn't flagged, cannot unflag
                print("Cannot remove flag from video: Video is not flagged")
                return

        # Video does not exist
        print("Cannot remove flag from video: Video does not exist")
