<template>
    <div>
      <h2>책 생성기</h2>
      <input v-model="topic" placeholder="주제를 입력하세요" @keydown.enter="generateBook" />
      <button @click="generateBook">책 생성</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  import { ref } from 'vue'
  
  export default {
    setup() {
      const topic = ref('')
      const router = useRouter()
  
      const generateBook = async () => {
        try {
            const response = await axios.post('http://localhost:8000/api/generate_book', { topic: topic.value })
            const bookText = response.data.text
            router.push({ name: 'BookResult', query: { topic: topic.value, text: bookText } })
        } catch (error) {
            console.error('Error generating book:', error)
        }
      }
  
      return { topic, generateBook }
    }
  }
  </script>
  