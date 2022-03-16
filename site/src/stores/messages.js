import { defineStore } from "pinia";

export const useToastStore = defineStore("toastMessages", {
    state: () => {
        return { errors: [] };
    },
    actions: {
        error(message) {
            const len = this.errors.push(message);
            setTimeout(() => {
                this.errors.splice(0, 1);
            }, 3000);
        }
    },
    getters: {
        errorList: (state) => state.errors
    }
});