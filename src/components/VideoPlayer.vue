<template>
  <div class="video-player-container">
    <div class="video-wrapper">
      <video ref="videoRef" :src="videoSrc" controls @loadedmetadata="handleVideoLoaded" @timeupdate="updateCurrentTime"></video>
      <div class="subtitle-box" v-for="(subtitle, index) in savedSubtitles" :key="index" :style="subtitleStyle(index)">
        {{ subtitle.text }}
      </div>
    </div>
    <div class="upload-button-container">
      <button class="upload-button" @click="reloadVideo">Upload Video</button>
      <input
        id="videoInput"
        ref="fileInput"
        type="file"
        style="display: none"
        @change="uploadVideo"
        accept="video/*"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['videoSrc'],
  data() {
    return {
      currentVideoTime: 0,
    };
  },
  computed: {
    savedSubtitles() {
      const storedSubtitles = localStorage.getItem('subtitles');
      return storedSubtitles ? JSON.parse(storedSubtitles) : [];
    },
  },
  methods: {
    reloadVideo() {
    this.openFileInput();
    this.clearLocalStorage();
  },
  clearLocalStorage() {
    localStorage.removeItem('subtitles');
    this.savedSubtitles = [];
  },
  openFileInput() {
    this.$refs.fileInput.click();
  },
    uploadVideo(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append('video', file);

      axios
        .post('http://localhost:5000/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then(response => {
          console.log(response.data.message); // Video uploaded successfully
          this.$emit('video-uploaded', file);
        })
        .catch(error => {
          console.error('Error uploading video:', error);
        });
    },
    handleVideoLoaded() {
      console.log("handleVideoLoaded called"); // Add this line to check if the method is being called

      // Update subtitle end times based on video duration
      this.savedSubtitles.forEach((subtitle, index) => {
        if (index < this.savedSubtitles.length - 1) {
          subtitle.endTime = this.savedSubtitles[index + 1].timestamp;
        } else {
          subtitle.endTime = subtitle.timestamp + subtitle.duration;
        }
      });
    },
    updateCurrentTime(event) {
      this.currentVideoTime = event.target.currentTime;
      console.log('Current video time:', this.currentVideoTime); // Debug statement
      this.displaySubtitles();
    },
    displaySubtitles() {

      console.log('displaySubtitles called');
      // Clear previous subtitles
      const subtitleElements = document.querySelectorAll('.subtitle-box');
      subtitleElements.forEach(subtitleElement => {
        subtitleElement.style.display = 'none';
      });

      // Display subtitles based on currentVideoTime
      this.savedSubtitles.forEach(subtitle => {
        console.log('Checking subtitle:', subtitle); // Debug statement
        if (this.currentVideoTime >= subtitle.timestamp && this.currentVideoTime <= subtitle.endTime) {
          console.log('Displaying subtitle:', subtitle); // Debug statement
          const subtitleElement = document.querySelector(`[data-subtitle-index="${subtitle.index}"]`);
          if (subtitleElement) {
            subtitleElement.style.display = 'block';
          }
        }
      });
    },
    subtitleStyle(index) {
      const subtitle = this.savedSubtitles[index];
      const topPosition = subtitle.top + 'px';
      const fontSize = subtitle.fontSize + 'px'; // Set the font size you want
      return {
        top: topPosition,
        fontSize: fontSize,
      };
    },
  },
};
</script>

<style scoped>
.video-player-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;   
  background-color: #f0f0f0;
  height: 100vh;
}

.video-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  background-color: black;
  overflow: hidden;
}

.video-wrapper video {
  width: 100%;
  height: auto;
}

.subtitle-box {
  position: absolute;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  display: block  ;
  white-space: pre-line;
  font-size: 18px;
}

.upload-button-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 10px;
}

.upload-button {
  font-size: 18px;
  font-weight: bold;
  color: white;
  background-color: #4CAF50;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  cursor: pointer;
}

.upload-button:hover {
  background-color: #45a049;
}
</style>
