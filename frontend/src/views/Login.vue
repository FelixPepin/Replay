<template>
    <div class="container mt-2">
        <div class="row">
            <div class="col-mb-3">
                <h1 class="mb-4">Connexion</h1>

                <div v-if="Object.keys(erreurs).length" class="alert alert-danger">
                    <ul class="mb-0">
                        <li v-for="(msg, champ) in erreurs" :key="champ">{{ msg }}</li>
                    </ul>
                </div>

                <form @submit.prevent="soumettre" action="/api/login" method="post" novalidate>
                    <div class="mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input v-model="email" type="email" id="email" class="form-control" />
                    </div>

                    <div class="mb-3">
                        <label for="password" class="form-label">Mot de passe</label>
                        <input v-model="password" type="password" id="password" class="form-control" />
                    </div>

                    <button type="submit" class="btn btn-primary w-100">Se connecter</button>

                    <p class="mt-3 text-center">
                        Pas de compte ?
                        <router-link to="/register">S'inscrire</router-link>
                    </p>
                </form>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()

const router = useRouter()

const email = ref('')
const password = ref('')
const erreurs = reactive({})
async function soumettre() {
    Object.keys(erreurs).forEach(k => delete erreurs[k])
    if (!email.value.trim()) erreurs.email = "L'adresse courriel est requise"
    if (!password.value.trim()) erreurs.password = "Le mot de passe est requis"

    if (Object.keys(erreurs).length > 0) return

    try {
        const reponse = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: email.value,
                password: password.value,
            })
        })

        const data = await reponse.json()

        if(reponse.ok){
            auth.connecter(data.token)
            router.push('/')
        } else{
            Object.assign(erreurs,data.erreurs)
        }
    }
    catch (e) {
        erreurs.serveur = "Impossible de contacter le serveur"
    }
}
</script>