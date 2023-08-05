<template>
  <div ref="root">
    <div
      :id="browserName"
      class="collapse"
      tabindex="-1"
      aria-labelledby="ref-modal-title"
      aria-hidden="true"
      ref="browser"
    >
      <div class="modal-dialog modal-dialog-scrollable modal-xl">
        <div class="modal-content">
          <div class="modal-header">Choose content</div>
          <div class="modal-body">
            <searchForm @search="search" @reset="reset" />
            <Breadcrumbs
              :breadcrumbs="breadcrumbs"
              :fetchData="fetchData"
              :portalURL="portalURL"
            />
            <Pagination
              v-if="data.batching"
              @next="fetchData"
              @previous="fetchData"
              :batching="data.batching"
            />
            total {{ data.items_total }}

            <ListItems
              :fetchData="fetchData"
              :items="data.items"
              :selectedItems="selected"
              :inputType="inputType"
              :selectableTypes="selectableTypes"
              :traversableTypes="traversableTypes"
              @checked="updateSelected"
            />
          </div>

          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-toggle="collapse"
              :data-bs-target="`#${browserName}`"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="widget-selected-items">
      <ul class="list-group">
        <li class="list-group-item" v-for="item in selected" :key="item">
          <input
            type="checkbox"
            checked
            :name="fieldName"
            :value="item.replace(portalURL, portalPath)"
          />
          {{ item }}
        </li>
      </ul>
    </div>
    <button
      type="button"
      class="btn btn-primary"
      data-bs-toggle="collapse"
      aria-expanded="false"
      :aria-controls="browserName"
      :data-bs-target="`#${browserName}`"
    >
      {{ buttonLable }}
    </button>
  </div>
</template>
<script>
import Pagination from "@/components/Pagination.vue";
import SearchForm from "@/components/searchForm.vue";
import Breadcrumbs from "@/components/Breadcrumbs.vue";
import ListItems from "@/components/ListItems.vue";

export default {
  components: {
    Pagination,
    SearchForm,
    Breadcrumbs,
    ListItems,
  },
  data() {
    return {
      open: false,
      // bootstrap: null,
      portalURL: "",
      baseURL: "",
      startURL: "",
      portalPath: "",
      fieldName: "",
      inputType: "",
      translations: {},
      data: {},
      breadcrumbs: [],
      selected: [],
      selectableTypes: [],
      traversableTypes: [],
      formData: {
        searchTerm: "",
        sortOn: "getObjPositionInParent",
        sortOrder: "ascending",
      },
    };
  },
  created() {
    this.baseURL = document.body.getAttribute("data-base-url");
    this.portalURL = document.body.getAttribute("data-portal-url");
  },
  mounted() {
    const wrapperElement = this.$refs.root.parentElement;
    this.startURL = wrapperElement.getAttribute("data-starturl");
    this.portalPath = wrapperElement.getAttribute("data-portalpath");
    this.fieldName = wrapperElement.getAttribute("data-fieldname");
    this.inputType = wrapperElement.getAttribute("data-inputtype");
    this.selectableTypes = JSON.parse(
      wrapperElement.getAttribute("data-selectabletypes")
    );
    this.traversableTypes = JSON.parse(
      wrapperElement.getAttribute("data-traversabletypes")
    );
    this.translations = JSON.parse(
      wrapperElement.getAttribute("data-translations")
    );

    this.loadSelectedItems(wrapperElement);

    this.$refs.browser.addEventListener("show.bs.collapse", () => {
      this.fetchData(this.startURL);
      this.open = true;
    });
    this.$refs.browser.addEventListener("hidden.bs.collapse", () => {
      this.open = false;
    });

    // this.loadBootstrap();
  },
  methods: {
    async fetchData(url, options) {
      let params = {
        metadata_fields: ["UID", "is_folderish", "portal_type"],
        sort_on: this.formData.sortOn,
        sort_order: this.formData.sortOrder,
      };

      if (!url) {
        url = this.data["@id"];
      }

      const isSearch = url.indexOf("/@search") != -1;

      if (options) {
        params = Object.assign(params, options);
      }

      if (!isSearch) {
        params.expand = "breadcrumbs";
      }

      const response = await this.axios.get(url, { params: params });

      this.data.items = response.data.items;
      this.data.items_total = response.data.items_total;
      this.data.batching = response.data.batching;

      if (!isSearch) {
        this.data["@id"] = response.data["@id"];
      }
      if (response.data["@components"]) {
        this.breadcrumbs = response.data["@components"].breadcrumbs.items;
      }
    },
    search(formData) {
      this.formData = Object.assign({}, this.formData, formData);
      const url = this.data["@id"] + "/@search";
      const currentURL = new URL(this.data["@id"]);
      let options = { "path.query": currentURL.pathname, "path.depth": 1 };
      if (this.formData.searchTerm.length > 2) {
        options.SearchableText = "*" + this.formData.searchTerm + "*";
        options["path.depth"] = -1;
      }
      this.fetchData(url, options);
    },
    reset(formData) {
      this.formData = formData;
      this.fetchData(this.startURL);
    },
    updateSelected(checked) {
      this.selected = checked;
      if (this.inputType == "radio") {
        window.jQuery.fn.collapse.Constructor.getInstance(this.$refs.browser).hide();
      }
    },
    loadSelectedItems(wrapperElement) {
      wrapperElement.parentElement
        .querySelectorAll(".selected_items input")
        .forEach((element) => {
          this.selected.push(
            this.portalURL + element.value.replace(this.portalPath, "")
          );
        });
      wrapperElement.parentElement.querySelector(".selected_items").remove();
    },
    // async loadBootstrap() {
    //   this.bootstrap = await import("bootstrap");
    // },
  },
  computed: {
    browserName() {
      return `reference-widget-browser-${this.fieldName.replace(/\./g, "_")}`;
    },
    buttonLable() {
      return this.open ? "Close" : "Browse";
    },
  },
};
</script>
