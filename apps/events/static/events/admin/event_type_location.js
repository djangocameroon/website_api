(function () {
    function toggleLocationField() {
        var typeField = document.getElementById("id_type");
        var locationRow = document.querySelector(".field-location");
        if (!typeField || !locationRow) {
            return;
        }
        locationRow.style.display = typeField.value === "Online" ? "none" : "";
    }

    document.addEventListener("DOMContentLoaded", function () {
        var typeField = document.getElementById("id_type");
        if (!typeField) {
            return;
        }
        toggleLocationField();
        typeField.addEventListener("change", toggleLocationField);
    });
})();
