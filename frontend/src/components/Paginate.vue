<template>
    <nav class="pagination is-small is-centered"
         role="navigation">
        <a class="pagination-previous"
           v-on:click.prevent="prev($event)"
           :disabled="isFirst">Previous</a>
        <ul class="pagination-list">
            <li v-for="button in buttons" v-bind:key="button.text">
                <a class="pagination-link"
                   :class="{'is-current': current === button.offset }"
                   v-on:click.prevent="goto(button.offset)"
                   v-if="button.offset !== null">{{ button.text }}</a>
                <span class="pagination-ellipsis"
                      v-if="button.offset === null">&hellip;</span>
            </li>
        </ul>
        <a class="pagination-next"
           v-on:click.prevent="next($event)"
           :disabled="isLast">Next</a>
    </nav>
</template>

<script>
    export default {
        name: 'Paginate',
        props: {
            total: Number,
            limit: Number,
            current: Number,
        },
        computed: {
            isFirst() {
                return this.$props.current === 0;
            },
            isLast() {
                return (this.$props.current + this.$props.limit) >= this.$props.total;
            },
            page() {
                return Math.ceil(this.$props.current / this.$props.total);
            },
            pages() {
                return Math.ceil(this.$props.total / this.$props.limit);
            },
            buttons() {
                const buttons = [];
                const page = this.$props.current / this.$props.limit;
                const pages = Math.ceil(this.$props.total / this.$props.limit);

                for (let i = 0; i < pages; i += 1) {
                    if (
                        i === 0 // first always
                        || (page === 0 && i === 2) // two after current if current is first
                        || i - 1 === page // one before current
                        || i === page // current
                        || i + 1 === page // one after current
                        || (page === pages - 1 && i === pages - 3) // two before last if last is active
                        || i === pages - 1) { // last page
                        buttons.push({
                            text: i + 1,
                            offset: i * this.$props.limit,
                        });
                    }
                }

                // left dots
                if (page > 2) {
                    buttons.splice(1, 0, { text: 'P', offset: null });
                }

                // right dots
                if (page < pages - 3) {
                    buttons.splice(buttons.length - 1, 0, { text: 'N', offset: null });
                }

                return buttons;
            },
        },
        methods: {
            goto(offset) {
                this.$emit('goto', offset);
            },
            prev(event) {
                if (event.target.hasAttribute('disabled')) return;
                this.$emit('goto', this.$props.current - this.$props.limit);
            },
            next(event) {
                if (event.target.hasAttribute('disabled')) return;
                this.$emit('goto', this.$props.current + this.$props.limit);
            },
        },
    };
</script>
