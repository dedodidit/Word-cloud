<template>
  <div id="container">
    <h1>Word Cloud Generator</h1>
    <form @submit.prevent="handle" method="post" enctype="multipart/form-data">
      <div class="upload">
        <label for="wine_mask">Upload Mask:</label>
        <input ref="wineMaskInput" type="file" name="wine_mask" accept=".png, .jpg, .jpeg" required>
      </div>
      <div class="text">
        <label for="text_input">Enter Text for Word Cloud:</label>
        <textarea ref="textInput" name="text_input" rows="4" required></textarea>
      </div>
      

        <button type="submit">Generate Word Cloud</button>
    </form>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';

const wineMaskInput = ref(null);
const textInput = ref(null);

const handle = async () => {
  try {
    const formData = new FormData();
    formData.append('wine_mask', wineMaskInput.value.files[0]);
    formData.append('text_input', textInput.value.value);

    const response = await axios.post('http://127.0.0.1:8000/generate_wordcloud/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      responseType: 'blob',
    });
    const blob = new Blob([response.data], { type: 'image/png' });
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = 'wordcloud.png';
    link.click();
    console.log(response.data);
  } catch (error) {
    console.error('Error submitting form:', error);
  }
};
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  margin: 20px;
}

h1 {
  text-align: center;
  color: #333;
}

form {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f4f4f4;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

label {
  display: block;
  margin-bottom: 10px;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
}

button {
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
