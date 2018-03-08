window.addEventListener("load", function() {
    // Define any functions that will need to be used throughout this file
    /**
     * Changes the theme to the given one, and puts the new one in localStorage
     * @param {String} theme
     */
    function changeTheme(theme) {
        // Add to this if we add more themes
        const themes = [
            // {% for theme in themes %}
                "$< theme.id >$",
            // {% endfor %}
        ];

        // First disable the themes that we don't want
        themes.filter(id => id !== theme).map(id => 
            // Disable the other theme sheets that are not the current one
            document.getElementById(id)
        ).forEach(element => element.disabled = true);

        //Also enable the stylesheet that we want to show
        document.getElementById(theme).disabled = false;


        window.localStorage.setItem("$< themeStorageKey >$", theme);
    }

    // Select the correct theme based on what's in local storage
    const theme = window.localStorage.getItem("$< themeStorageKey >$") || "LightTheme";

    changeTheme(theme);
});
