<template>
  <div>
    <h1>PDF 업로드 및 변환</h1>
    <input type="file" @change="handleFileUpload" />
    <div v-if="pdfData">
      <h2>PDF 내용</h2>
      <div v-for="(text, index) in pdfData.text" :key="index">
        <h3>페이지 {{ index + 1 }}</h3>
        <div v-html="text"></div>
        <div v-for="(image, imgIndex) in pdfData.images" :key="imgIndex">
          <img :src="`http://localhost:8000/images/${image}`" alt="PDF 이미지" />
        </div>
      </div>
    </div>

    <h2>학생과의 상호 소통</h2>
    <input v-model="studentPrompt" placeholder="학생의 질문을 입력하세요" />
    <button @click="sendPrompt">질문 보내기</button>
    <div v-if="studentResponse">
      <h3>OpenAI의 응답</h3>
      <p>{{ studentResponse }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      pdfData: null,
      studentPrompt: '',
      studentResponse: ''
    }
  },
  methods: {
    async handleFileUpload(event) {
      const file = event.target.files[0]
      const formData = new FormData()
      formData.append('file', file)

      try {
        const response = await axios.post('http://localhost:8000/extract', formData)
        this.pdfData = response.data
      } catch (error) {
        console.error('Error uploading file:', error)
      }
    },
    async sendPrompt() {
      try {
        const response = await axios.post('http://localhost:8000/chat', { prompt: this.studentPrompt })
        this.studentResponse = response.data.response
      } catch (error) {
        console.error('Error sending prompt:', error)
      }
    }
  }
}
</script>

<style>
/* 스타일을 추가하여 UI를 개선합니다 */
h1, h2, h3 {
  font-family: Arial, sans-serif;
  color: #333;
}

input[type="file"] {
  margin-bottom: 20px;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 10px 0;
}

input[type="text"] {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

button:hover {
  background-color: #ddd;
}

p {
  font-size: 16px;
  line-height: 1.5;
}
</style>
