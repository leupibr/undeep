<template>
    <div class="container">
        <div class="content">
            <label>
                <input class="title input is-fullwidth"
                       type="text"
                       v-if="details"
                       v-model="details.name"
                       @change="changeName()"
                />
            </label>
        </div>
        <div class="content" v-if="details">
            <div class="buttons is-right">
                <a class="button"
                   target="_blank"
                   :href="this.download">
                    <span class="icon"><i class="fas fa-download"></i></span>
                    <span>Download</span>
                </a>
                <a class="button is-danger" v-on:click="confirmDelete()">
                    <span class="icon"><i class="fas fa-trash"></i></span>
                    <span>Delete</span>
                </a>
            </div>
        </div>
        <div class="content" v-if="details">
            <table class="table is-narrow is-fullwidth">
                <tr>
                    <th><label for="category">Category</label></th>
                    <td>
                        <div class="field has-addons">
                            <div class="control">
                                <div class="select" v-bind:class="{'is-loading': categories === null}">
                                    <select id="category" v-model="details.category" @change="changeCategory()">
                                        <option disabled value="null">Please select a category</option>
                                        <option v-for="c in categories"
                                                v-bind:key="c.name"
                                                v-bind:value="c.name">
                                            {{c.name}}
                                        </option>
                                    </select>
                                </div>
                            </div>
                            <div class="control">
                                <a class="button is-static" v-if="details.method === 'Manual'">
                                    <i class="fas fa-user-tag"></i>
                                </a>
                                <a class="button is-static" v-if="details.method === 'Confirmed'">
                                    <i class="fas fa-user-check"></i>
                                </a>
                                <a class="button is-warning"
                                   v-if="details.method === 'Automatic'"
                                   v-on:click="this.confirmCategory">
                                    <i class="fas fa-robot"></i>
                                </a>
                            </div>
                        </div>
                    </td>
                </tr>
                <tr>
                    <th>Date</th>
                    <td>
                        <datepicker v-model="details.date"
                                    id="date" name="date"
                                    format="MMMM dd, yyyy"
                                    :typeable="true"
                                    :monday-first="true"
                                    :use-utc="true"
                                    wrapper-class="control"
                                    @input="changeDate()"
                                    :highlighted="details.alt_dates"
                                    input-class="input">
                        </datepicker>
                    </td>
                </tr>
                <tr>
                    <th>Size</th>
                    <td>{{details.size|humanize(false, 2)}}</td>
                </tr>
                <tr>
                    <th>Modified</th>
                    <td>{{details.uploaded|moment('llll')}}</td>
                </tr>
                <tr>
                    <th>Uploaded</th>
                    <td>{{details.modified|moment('llll')}}</td>
                </tr>
            </table>
        </div>
        <div class="content">
            <embed :src="this.preview"
                   class="box" style="width:100%;height:100vh;" type="application/pdf"/>
        </div>

        <DeleteConfirmation
            :title="`Delete ${details.name}?`"
            @confirm="deleteDocument"
            @abort="showConfirmation = false"
            v-if="showConfirmation">
            <p>Do you really want to delete this category <b>irreversible</b>?</p>
        </DeleteConfirmation>
    </div>
</template>

<script>
    import Datepicker from 'vuejs-datepicker';
    import axios from 'axios';
    import DeleteConfirmation from './DeleteConfirmation';

    export default {
        name: 'ViewDocument',
        components: { DeleteConfirmation, Datepicker },
        data() {
            return {
                details: null,
                categories: null,
                showConfirmation: false,
            };
        },
        computed: {
            download() {
                return `${axios.defaults.baseURL}documents/${this.$route.params.id}/download`;
            },
            preview() {
                return `${axios.defaults.baseURL}documents/${this.$route.params.id}/preview#view=FitH`;
            },
        },
        methods: {
            loadDetails() {
                axios.get(`documents/${this.$route.params.id}`)
                    .then((response) => {
                        this.details = response.data;
                        if (!this.details.alt_dates) return;

                        const dates = [];
                        this.details.alt_dates.forEach((d) => {
                            dates.push(new Date(`${d}Z`));
                        });
                        this.details.alt_dates = { dates };
                    });
            },
            loadCategories() {
                axios.get('categories')
                    .then((response) => {
                        this.categories = response.data;
                    });
            },
            changeCategory() {
                axios.post(`categories/${this.details.category}/assign`, {
                    document: this.details.path,
                });
            },
            confirmCategory() {
                axios.put(`documents/${this.$route.params.id}/confirm`)
                    .then(() => {
                        this.details.method = 'Confirmed';
                    });
            },
            changeName() {
                axios.post(`documents/${this.$route.params.id}`, this.details);
            },
            changeDate() {
                axios.post(`documents/${this.$route.params.id}/details`, this.details);
            },
            confirmDelete() {
                this.showConfirmation = true;
            },
            deleteDocument() {
                axios.delete(`documents/${this.$route.params.id}`)
                    .then(() => {
                        this.$router.go(-1);
                    });
            },
        },
        beforeMount() {
            this.loadCategories();
            this.loadDetails();
        },
    };
</script>
