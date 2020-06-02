<template>
  <div>
    <form id="file-drag-drop" ref="fileform" class="box has-text-grey-light">
      <span class="drop-files">
        <i class="fas fa-upload fa-4x"></i>
      </span>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Upload',
  data() {
    return {
      dragAndDropCapable: false,
      files: [],
    };
  },
  methods: {
    determineDragAndDropCapable() {
      const div = document.createElement('div');
      return (('draggable' in div)
        || ('ondragstart' in div && 'ondrop' in div))
        && 'FormData' in window && 'FileReader' in window;
    },
    uploadFiles() {
      const data = new FormData();
      for (let i = 0; i < this.files.length; i += 1) {
        const file = this.files[i];
        data.append(`files[${i}]`, file);
      }
      axios.post('documents/upload', data,
        { headers: { 'Content-Type': 'multipart/form-data' } })
        .then((response) => {
          const uploaded = response.data;
          if (uploaded.length === 1) {
            this.$router.push({ name: 'ViewDocument', params: { id: uploaded[0].path } });
          } else {
            this.$eventBus.$emit('store-changed');
          }
        });
      this.files = [];
    },
  },
  mounted() {
    this.dragAndDropCapable = this.determineDragAndDropCapable();
    if (!this.dragAndDropCapable) return;
    ['drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop'].forEach((evt) => {
      this.$refs.fileform.addEventListener(evt, (e) => {
        e.preventDefault();
        e.stopPropagation();
      }, false);
    });

    this.$refs.fileform.addEventListener('drop', (e) => {
      for (let i = 0; i < e.dataTransfer.files.length; i += 1) {
        this.files.push(e.dataTransfer.files[i]);
      }
      this.uploadFiles();
    });
  },

};
</script>

<style scoped>
  #file-drag-drop {
    border-style: dotted;
    position: fixed;
    right: 1rem;
    bottom: 1rem;
  }
</style>
