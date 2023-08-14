<template>
  <div id="app">
    <div class="video-container">
      <VideoPlayer :videoSrc="videoSrc" @video-uploaded="handleVideoUploaded" />
    </div>
    <div class="upload-form">
      <div class="upload-button-container">
        
        <input
          id="videoInput"
          ref="fileInput"
          type="file"
          style="display: none"
          @change="uploadVideo"
          accept="video/*"
        />
      </div>
      <input v-model="customFilePath" placeholder="Custom File Path (Optional)" />
    </div>
    <SubtitleEditor :subtitles="subtitles" />
  </div>
</template>

<script>
import SubtitleEditor from './components/SubtitleEditor.vue';
import VideoPlayer from './components/VideoPlayer.vue';
import axios from 'axios';

export default {
  name: 'App',
  components: {
    SubtitleEditor,
    VideoPlayer,
  },
  data() {
    return {
      subtitles: [],
      videoSrc: '',
      customFilePath: '',
    };
  },
  methods: {
    handleVideoUploaded(file) {
      this.videoSrc = URL.createObjectURL(file);
    },
    openFileInput() {
      this.$refs.videoPlayer.openFileInput();
    },
    uploadVideo(event) {
      const file = event.target.files[0];
      if (file) {
        const formData = new FormData();
        formData.append('video', file);
        formData.append('file_path', this.customFilePath);

        axios
          .post('http://localhost:5000/api/upload', formData, {
            withCredentials: true,
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          })
          .then(response => {
            console.log(response.data.message); // Video uploaded successfully
            this.handleVideoUploaded(file); // Update videoSrc to display the uploaded video
          })
          .catch(error => {
            console.error('Error uploading video:', error);
          });
      }
    },
  },
};
</script>


<style>
#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f0f0;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

.video-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: auto; 
  width: 100%;
  overflow: hidden;
  margin-bottom: 10px;
}

.upload-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

/* .content-wrapper {
  max-width: 100vw;
  padding: 20px;
  
} */
</style>