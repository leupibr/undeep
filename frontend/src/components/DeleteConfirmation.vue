<template>
    <div class="modal is-active">
        <div class="modal-background" v-on:click="abort"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title">{{title}}</p>
                <a class="delete"
                   v-on:click="abort"
                   aria-label="close"></a>
            </header>
            <section class="modal-card-body">
                <slot></slot>
            </section>
            <footer class="modal-card-foot">
                <a class="button is-danger"
                   v-on:click="confirm">Yes</a>
                <a class="button"
                   v-on:click="abort">Cancel</a>
            </footer>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'DeleteConfirmation',
        props: {
            title: { type: String, required: true },
        },
        methods: {
            abort() {
                this.$emit('abort');
            },
            confirm() {
                this.$emit('confirm');
            },
        },
    };
</script>

<style scoped>

</style>
