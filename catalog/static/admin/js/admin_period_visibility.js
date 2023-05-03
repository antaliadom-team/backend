document.addEventListener('DOMContentLoaded', function () {
    function updatePeriodVisibility() {
        const categorySelect = document.querySelector('#id_category');
        const periodField = document.querySelector('#id_period');
        const periodRow = periodField.closest('.field-period');

        const selectedText = categorySelect.options[categorySelect.selectedIndex].text;

        if (selectedText === "Аренда") {
            periodRow.style.display = '';
        } else {
            periodRow.style.display = 'none';
        }
    }

    const categorySelect = document.querySelector('#id_category');
    categorySelect.addEventListener('change', updatePeriodVisibility);

    updatePeriodVisibility();
});
