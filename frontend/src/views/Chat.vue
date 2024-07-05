// frontend/src/views/Chat.vue
<template>
  <h2>질의응답</h2>
  <input 
    v-model="studentPrompt" 
    placeholder="학생의 질문을 입력하세요"
    @keydown.enter="sendPrompt" />
  <button @click="sendPrompt">질문 보내기</button>
  <div v-if="studentResponse">
    <h3>OpenAI의 응답</h3>
    <p>{{ studentResponse }}</p>
  </div>
  
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      studentPrompt: '',
      studentResponse: ''
    }
  },
  methods: {
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
section {
  padding: 20px;
  background: white;
  margin: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
}

button:hover {
  background-color: #ddd;
}

p {
  font-size: 16px;
  line-height: 1.5;
}
</style>
