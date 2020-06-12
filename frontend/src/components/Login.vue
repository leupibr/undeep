<template>
    <section class="hero">
        <div class="hero-body">
            <div class="container">
                <div class="columns is-centered">
                    <div class="column is-4 box">
                        <div class="field">
                            <label for="username" class="label">Username</label>
                            <div class="control has-icons-left">
                                <input id="username" name="username" type="text" v-model="username"
                                       placeholder="johndoe" class="input" required>
                                <span class="icon is-small is-left">
                                    <i class="fa fa-user-circle"></i>
                                </span>
                            </div>
                        </div>
                        <div class="field">
                            <label for="password" class="label">Password</label>
                            <div class="control has-icons-left">
                                <input id="password" name="password" type="password" v-model="password"
                                       placeholder="*******" class="input" required>
                                <span class="icon is-small is-left">
                                    <i class="fa fa-lock"></i>
                                </span>
                            </div>
                        </div>
                        <div class="field">
                            <button class="button is-success" v-on:click="login()">Login</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
    import auth from '../services/auth';

    export default {
        name: 'Login',
        data() {
            return {
                username: '',
                password: '',
            };
        },
        methods: {
            async login() {
                const credentials = {
                    username: this.username,
                    password: this.password,
                };
                let response;
                try {
                    response = await auth.login(credentials);
                } catch (error) {
                    this.$notify({
                        text: error.response.data.message,
                        type: 'is-danger',
                    });
                    return;
                }
                const { token, user } = response;
                await this.$store.dispatch('login', { token, user });
                await this.$router.replace({ name: 'Home' });
            },
        },
    };
</script>

<style scoped>

</style>
