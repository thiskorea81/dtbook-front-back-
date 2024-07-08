<template>
    <div>
      <h2>Generated Book</h2>
      <div v-html="formattedText"></div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue'
  import { useRoute } from 'vue-router'
  
  export default {
    setup() {
      const route = useRoute()
      const text = ref(route.query.text || '')
      const formattedText = ref('')
  
      const formatText = (text) => {
        const lines = text.split('\n')
        let formattedText = ''
        lines.forEach(line => {
          if (line.startsWith('```')) {
            formattedText += '<pre><code>' + line.replace(/```/g, '') + '</code></pre>'
          } else {
            formattedText += '<p>' + line + '</p>'
          }
        })
        return formattedText
      }
  
      formattedText.value = formatText(text.value)
  
      return { formattedText }
    }
  }
  </script>
  
  <style scoped>
  pre {
    background-color: #f4f4f4;
    padding: 10px;
    border-radius: 5px;
    overflow: auto;
  }
  code {
    font-family: monospace;
  }
  p {
    font-family: Arial, sans-serif;
    line-height: 1.6;
  }
  </style>
  