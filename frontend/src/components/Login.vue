<template>
    <section class="hero">
        <div class="hero-body">
            <div class="container">
                <div class="columns is-centered">
                    <div class="column is-4 box">
                        <login-field
                            label="Username"
                            name="username"
                            type="text"
                            placeholder="j.doe"
                            icon="fa fa-user-circle"
                            v-model="username"/>
                        <login-field
                            label="Password"
                            name="password"
                            type="password"
                            placeholder="*******"
                            icon="fa fa-lock"
                            v-model="password"/>
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
    import Vue from 'vue';
    import auth from '../services/auth';

    Vue.component('login-field', {
        props: ['value', 'label', 'name', 'type', 'placeholder', 'icon'],
        template: `
            <div class="field">
                <label :for="name" class="label">{{label}}</label>
                <div class="control has-icons-left">
                    <input :id="name" :name="name" :type="type" :placeholder="placeholder"
                           :value="value" @input="$emit('input', $event.target.value)"
                           class="input" required>
                    <span class="icon is-small is-left"><i :class="icon"></i></span>
                </div>
            </div>
        `,
    });

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
