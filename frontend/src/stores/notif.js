import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useNotifStore = defineStore('notif', () => {
  const message = ref('')
  const type = ref('success')

  function setNotif(msg, t = 'success') {
    message.value = msg
    type.value = t
  }

  function clear() {
    message.value = ''
  }

  return { message, type, setNotif, clear }
})
