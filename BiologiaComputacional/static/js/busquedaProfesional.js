// Variables globales
let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
  columnDefs: [
    { className: "centered", targets: [0, 1, 2, 3] },
    { orderable: false, targets: [3] },
  ],
  pageLength: 5,
  destroy: true,
  lengthMenu: [
    [5, 25, 50, -1],
    [5, 25, 50, "Todos"],
  ],
  language: {
    url: "//cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json",
  },
};

const infoProfesional = async () => {
  try {
    const response = await fetch(
      "http://127.0.0.1:8000/profesionales/info_profesional/"
    );
    const data = await response.json();

    $(".view-button").click(function () {
      const profesionalId = $(this).data("id");
      window.location.href = `/profesionales/id=${profesionalId}/`;
    });
  } catch (ex) {
    alert(ex);
  }
};
