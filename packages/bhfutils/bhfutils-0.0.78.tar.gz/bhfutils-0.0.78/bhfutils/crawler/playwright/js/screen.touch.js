if (opts.max_touch_points) {
    Object.defineProperty(Object.getPrototypeOf(navigator), 'maxTouchPoints', {
        get: () => opts.max_touch_points,
    })
    Object.defineProperty(window, 'ontouchstart', {
        writable: true,
        enumerable: true,
        configurable: false, // note!
        value: {} // We'll extend that later
    })
}
