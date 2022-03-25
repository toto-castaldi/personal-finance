export default {
    isIterable: (obj) => {
        if (obj == null) {
            return false;
        }
        return typeof obj[Symbol.iterator] === 'function';
    },
    emailValid: (email) => {
        return String(email)
            .toLowerCase()
            .match(
                /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            );
    },
    mathMap: (inNum, in_min, in_max, out_min, out_max) => {
        return (inNum - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
    }
}