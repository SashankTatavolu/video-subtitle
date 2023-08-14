<template>
  <div class="subtitle-editor-container">
    <div
      v-for="(subtitle, index) in subtitles"
      :key="index"
      class="subtitle"
      :style="{ top: subtitle.top + 'px' }"
    >
      {{ subtitle.text }}
      <span class="handle" @mousedown="startDrag(subtitle, index,$event)">🔳</span>
    </div>

    <!-- Create Subtitle Form -->
    <div class="create-subtitle-form">
      <input v-model="newSubtitle.text" placeholder="Subtitle text" />
      <input v-model="newSubtitle.timestamp" type="number" placeholder="Timestamp (in seconds)" />
      <button @click="addSubtitle">Create Subtitle</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    subtitles: Array,
    videoId: String,
  },
  data() {
    return {
      dragging: false,
      dragIndex: null,
      dragOffsetY: 0,
      localSubtitles: [], 
      newSubtitle: {
        text: '',
        timestamp: 0,
      },
    };
  },
  methods: {
    startDrag(subtitle, index, event) {
      this.dragging = true;
      this.dragIndex = index;
      this.dragOffsetY = event.clientY - subtitle.top;
    },
    stopDrag() {
      this.dragging = false;
      this.dragIndex = null;
    },
    handleDrag(event) {
    if (this.dragging) {
      const newY = event.clientY - this.dragOffsetY;
      this.localSubtitles = this.localSubtitles.map((subtitle, index) => {
        if (index === this.dragIndex) {
          return { ...subtitle, top: newY };
        }
        return subtitle;
      });
    }
  },
  addSubtitle() {
      axios
        .post('http://localhost:5000/api/create_subtitle', {
          video_id: 'your_video_id', // Replace with the actual video ID
          subtitle_text: this.newSubtitle.text,
          timestamp: this.newSubtitle.timestamp,
        })
        .then((response) => {
          console.log(response.data.message); // Subtitle created successfully

          // Update the localSubtitles array with the newly created subtitle
          const newSubtitle = {
            text: this.newSubtitle.text,
            timestamp: this.newSubtitle.timestamp,
            top: 0, // Set the initial top value here
          };
          this.localSubtitles.push(newSubtitle);

          // Clear the newSubtitle data
          this.newSubtitle.text = '';
          this.newSubtitle.timestamp = 0;

          // Save updated subtitles to local storage
          localStorage.setItem('subtitles', JSON.stringify(this.localSubtitles));

          // Emit an event to update the parent's subtitles prop if needed
          this.$emit('updateSubtitles', this.localSubtitles);
        })
        .catch((error) => {
          console.error('Error creating subtitle:', error);
        });
        if (this.localSubtitles.length > 0) {
    const lastSubtitle = this.localSubtitles[this.localSubtitles.length - 1];
    this.newSubtitle.duration = this.newSubtitle.timestamp - lastSubtitle.timestamp;
  } else {
    this.newSubtitle.duration = 0; // For the first subtitle
  }

  // Push the new subtitle into the localSubtitles array
  this.localSubtitles.push({
    text: this.newSubtitle.text,
    timestamp: this.newSubtitle.timestamp,
    top: 0, // You can set this value as needed
    duration: this.newSubtitle.duration,
  });
    },
    
  },
  mounted() {
    // Initialize localSubtitles with a deep copy of the subtitles prop
    this.localSubtitles = JSON.parse(JSON.stringify(this.subtitles));
    window.addEventListener('mousemove', this.handleDrag);
    window.addEventListener('mouseup', this.stopDrag);
  },
  beforeUnmount() {
    window.removeEventListener('mousemove', this.handleDrag);
    window.removeEventListener('mouseup', this.stopDrag);
  },
};
</script>

<style scoped>
.subtitle {
  position: absolute;
  cursor: grab;
}

.handle {
  cursor: grab;
  margin-left: 8px; 
}

.subtitle-editor-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.create-subtitle-form {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
