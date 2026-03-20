<template>
  <div class="container mt-2">
    <div class="row">
      <div class="col-mb-3">
        <h1 class="mb-4">Créer un compte</h1>

        <div v-if="Object.keys(erreurs).length" class="alert alert-danger">
          <ul class="mb-0 list-unstyled">
            <li v-for="(msg, champ) in erreurs" :key="champ">- {{ msg }}</li>
          </ul>
        </div>

        <form @submit.prevent="soumettre" method="post" action="/api/register" novalidate>
          <div class="mb-3">
            <label for="username" class="form-label">Nom d'utilisateur</label>
            <input
              v-model="username"
              type="text"
              id="username"
              name="username"
              class="form-control"
            />
          </div>

          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input v-model="email" type="email" id="email" name="email" class="form-control" />
          </div>

          <div class="mb-3">
            <label for="password" class="form-label">Mot de passe</label>
            <input
              v-model="password"
              type="password"
              id="password"
              name="password"
              class="form-control"
            />
          </div>

          <div class="mb-3">
            <label for="confirm" class="form-label">Confirmer le mot de passe</label>
            <input
              v-model="confirm"
              type="password"
              id="confirm"
              name="confirm"
              class="form-control"
            />
          </div>

          <button type="submit" class="btn btn-primary w-100">S'inscrire</button>

          <p class="mt-3 text-center">
            Déjà un compte ?
            <router-link to="/login">Se connecter</router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useNotifStore } from '@/stores/notif'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const notif = useNotifStore()
const auth = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const confirm = ref('')
const erreurs = reactive({})
let regexCourriel = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/
let regexMdp = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/

async function soumettre() {
  Object.keys(erreurs).forEach((k) => delete erreurs[k])

  if (!username.value.trim()) erreurs.username = "Le nom d'utilisateur est requis"
  if (!email.value.trim()) erreurs.email = "L'adresse courriel est requise"
  else if (!regexCourriel.test(email.value))
    erreurs.email = "L'adresse courriel doit avoir le format suivant (exemple@exemple.com)"
  if (!password.value) erreurs.password = 'Le mot de passe est requis'
  else if (!regexMdp.test(password.value))
    erreurs.password =
      'Le mot de passe doit contenir huit caractères, au moins une minuscule, majuscule, un chiffre et un caractère spécial'
  if (password.value !== confirm.value)
    erreurs.confirm = 'Les deux mots de passe doivent correspondre'

  if (Object.keys(erreurs).length > 0) return

  try {
    const reponse = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value,
        confirm: confirm.value,
      }),
    })

    const data = await reponse.json()

    if (reponse.ok) {
      localStorage.setItem('token', data.token)
      auth.connecter(data.token)
      notif.setNotif('Compte créé avec succès ! Bienvenue sur RePlay.')
      router.push('/')
    } else {
      Object.assign(erreurs, data.erreurs)
    }
  } catch (e) {
    erreurs.serveur = 'Impossible de contacter le serveur'
  }
}
</script>
