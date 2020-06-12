<template>
    <div id="login">
        <h1>Login</h1>
        <input type="text" name="username" v-model="username" placeholder="Username"/>
        <input type="password" name="password" v-model="password" placeholder="Password"/>
        <button type="button" v-on:click="login()">Login</button>
    </div>
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
