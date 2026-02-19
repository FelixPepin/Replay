<template>
    <div class="container mt-2">
        <div class="row">
            <div class="col-mb-3">
                <h1 class="mb-4">Créer un compte</h1>

                <!-- <div class="alert alert-danger"></div>
                <div class="alert alert-success"></div> -->

                <form>
                    <div class="mb-3">
                        <label for="username" class="form-label">Nom d'utilisateur</label>
                        <input type="text" id="username" class="form-control" required />
                    </div>

                    <div class="mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input type="email" id="email" class="form-control" required />
                    </div>

                    <div class="mb-3">
                        <label for="password" class="form-label">Mot de passe</label>
                        <input type="password" id="password" class="form-control" required />
                    </div>

                    <div class="mb-3">
                        <label for="confirm" class="form-label">Confirmer le mot de passe</label>
                        <input type="password" id="confirm" class="form-control" required />
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
