if (opts.navigator_platform) {
    utils.replaceProperty(Object.getPrototypeOf(navigator), 'platform', {
            get() {
                return opts.navigator_platform
            }
        })
}
