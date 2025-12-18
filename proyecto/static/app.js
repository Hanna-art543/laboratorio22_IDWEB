document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('equipo-form');
    const tabla = document.querySelector('#tabla-equipos tbody');
    const btnBuscar = document.getElementById('btn-buscar');
    const inputBusqueda = document.getElementById('busqueda-id');
    const resultadoBusqueda = document.getElementById('resultado-busqueda');

    const cargarEquipos = async () => {
        const res = await fetch('/equipos');
        const equipos = await res.json();
        tabla.innerHTML = '';
        equipos.forEach(eq => {
            tabla.innerHTML += `
                <tr>
                    <td>${eq.id}</td>
                    <td>${eq.nombre}</td>
                    <td>${eq.ciudad}</td>
                    <td>${eq.nivelAtaque}</td>
                    <td>${eq.nivelDefensa}</td>
                </tr>`;
        });
    };

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const nuevo = {
            nombre: document.getElementById('nombre').value,
            ciudad: document.getElementById('ciudad').value,
            nivelAtaque: parseInt(document.getElementById('ataque').value),
            nivelDefensa: parseInt(document.getElementById('defensa').value)
        };

        const res = await fetch('/equipos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(nuevo)
        });

        if (res.ok) {
            form.reset();
            cargarEquipos();
        }
    });

    btnBuscar.addEventListener('click', async () => {
        const id = inputBusqueda.value;
        if (!id) return;

        const res = await fetch(`/equipos/${id}`);
        if (res.status === 200) {
            const eq = await res.json();
            resultadoBusqueda.innerHTML = `Encontrado: ${eq.nombre} (${eq.ciudad})`;
        } else {
            resultadoBusqueda.innerHTML = `Error: Equipo no encontrado (404)`;
        }
    });

    cargarEquipos();
});