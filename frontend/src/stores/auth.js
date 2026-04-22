import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token'))

  const utilisateur = computed(() => {
    if (!token.value) {
      return null
    } else {
      try {
        const payload = JSON.parse(atob(token.value.split('.')[1]))
        return payload
      } catch {
        return null
      }
    }
  })

  const estConnecte = computed(() => !!token.value)
  const userId = computed(() => utilisateur.value?.utilisateur_id ?? null)
  const role = computed(() => utilisateur.value?.role ?? null)

  function connecter(nouveauToken) {
    token.value = nouveauToken
    localStorage.setItem('token', nouveauToken)
  }

  function deconnecter() {
    token.value = null
    localStorage.removeItem('token')
  }

  const nom = computed(() => utilisateur.value?.nomUtilisateur ?? 'Utilisateur')

  const initiales = computed(() => {
    const username = utilisateur.value?.nomUtilisateur ?? ''
    return username.charAt(0).toUpperCase() || '?'
  })

  return { token, estConnecte, utilisateur, userId, role, nom, initiales, connecter, deconnecter }
})
