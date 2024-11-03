// Variables globales
let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3] },
        { orderable: false, targets: [2, 3] }
    ],
    pageLength: 5,
    destroy: true,
    "lengthMenu": [[5, 25, 50, -1], [5, 25, 50, "Todos"]],
    "language": {
        "url": "//cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json"
    }
};

const infoUsers = async () => {
    try {

        const response = await fetch("http://127.0.0.1:8000/identity/info_usuarios/");
        const data = await response.json();

        let content = ``;

        data.info_users.forEach((info) => {
            content += `
                <tr>
                    <td>${info.username}</td>
                    <td>${info.first_name + " " + info.last_name}</td>
                    <td>
                        ${info.is_superuser ? '<span class="badge rounded-1 text-bg-success">Super usuario</span>' : ''}
                        ${info.is_staff ? '<span class="badge rounded-1 text-bg-primary">Administrador</span>' : ''}
                        ${!info.is_superuser && !info.is_staff ? '<span class="badge rounded-1 text-bg-secondary">Estudiante</span>' : ''}
                    </td>
                    <td>
                        <button class = 'btn btn-sm view-button' style = 'color: #38B7E0' data-id='${info.id}'><i class = 'fa-solid fa-arrow-right'></i></button>
                    </td>
                </tr>
            `;
        });
        tableBody.innerHTML = content;

        $('.view-button').click(function () {

            const userID = $(this).data('id');

            window.location.href = `/identity/detalle_usuarios/id=${userID}/`;

        });
    } catch (ex) {
        alert(ex);
    }
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await infoUsers();

    dataTable = $('#info').dataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

window.addEventListener("load", async () => {
    await initDataTable();
});

