export default {
    isIterable: (obj) => {
        if (obj == null) {
            return false;
        }
        return typeof obj[Symbol.iterator] === 'function';
    }
}