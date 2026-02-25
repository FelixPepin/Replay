import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
    const token = ref(localStorage.getItem('token'))

    const estConnecte = computed(() => !!token.value)

    function connecter(nouveauToken) {
        token.value = nouveauToken
        localStorage.setItem('token', nouveauToken)
    }

    function deconnecter() {
        token.value = null
        localStorage.removeItem('token')
    }

    return { token, estConnecte, connecter, deconnecter }
})