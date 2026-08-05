(function () {
    function toggleSpeakersAndTagsFields() {
        var linkField = document.getElementById("id_external_registration_link");
        var parentFieldset = document.querySelector("fieldset.module:has(.field-speakers, .field-tags)");
        var speakersRow = document.querySelector(".field-speakers");
        var tagsRow = document.querySelector(".field-tags");
        if (!linkField) {
            return;
        }
        var hasLink = linkField.value.trim() !== "";
        const linkRegex = /^(https?:\/\/)?([\w-]+(\.[\w-]+)+)(\/[\w-]*)*(\?.*)?(#.*)?$/;
        if (hasLink && !linkRegex.test(linkField.value.trim())) {
            hasLink = false;
        }
        if (speakersRow) {
            speakersRow.style.display = hasLink ? "none" : "";
        }
        if (tagsRow) {
            tagsRow.style.display = hasLink ? "none" : "";
        }
        if (parentFieldset) {
            parentFieldset.style.display = hasLink ? "none" : "";
        }
    }

    document.addEventListener("DOMContentLoaded", function () {
        var linkField = document.getElementById("id_external_registration_link");
        if (!linkField) {
            return;
        }
        toggleSpeakersAndTagsFields();
        linkField.addEventListener("input", toggleSpeakersAndTagsFields);
    });
})();
