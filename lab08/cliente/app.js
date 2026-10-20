const API = 'http://127.0.0.1:8000/api';
const $ = (id) => document.getElementById(id);

function mostrarAlerta(texto, tipo) {
  const a = $('alerta');
  a.textContent = texto;
  a.className = 'alerta ' + tipo;
  a.hidden = false;
  setTimeout(() => (a.hidden = true), 6000);
}

function formatearErrores(data) {
  if (typeof data !== 'object' || data === null) return String(data);
  if (data.detail) return data.detail;
  return Object.entries(data)
    .map(([campo, msgs]) => `${campo}: ${[].concat(msgs).join(' ')}`)
    .join('\n');
}

async function peticion(ruta, metodo = 'GET', cuerpo = null) {
  const headers = { 'Content-Type': 'application/json' };
  const token = localStorage.getItem('token');
  if (token && ruta !== '/login/') headers['Authorization'] = 'Token ' + token;

  const resp = await fetch(API + ruta, {
    method: metodo,
    headers,
    body: cuerpo ? JSON.stringify(cuerpo) : null,
  });
  const data = resp.status === 204 ? null : await resp.json().catch(() => null);
  if (!resp.ok) {
    const err = new Error(formatearErrores(data));
    err.status = resp.status;
    throw err;
  }
  return data;
}

function actualizarSesion() {
  const logueado = !!localStorage.getItem('token');
  $('form-login').hidden = logueado;
  $('sesion').hidden = !logueado;
}

function crearCard(titulo, lineas, etiqueta) {
  const card = document.createElement('div');
  card.className = 'card';
  const h = document.createElement('h3');
  h.textContent = titulo;
  card.appendChild(h);
  lineas.forEach((t) => {
    const p = document.createElement('p');
    p.textContent = t;
    card.appendChild(p);
  });
  if (etiqueta) card.appendChild(etiqueta);
  return card;
}

async function cargarEspacios() {
  const espacios = await peticion('/espacios/');
  const lista = $('lista-espacios');
  const select = $('r-espacio');
  lista.innerHTML = '';
  select.innerHTML = '';

  espacios.forEach((e) => {
    const tag = document.createElement('span');
    tag.className = 'tag ' + (e.estado_operativo ? 'ok' : 'off');
    tag.textContent = e.estado_operativo ? 'Operativo' : 'Inactivo';
    lista.appendChild(
      crearCard(e.nombre, [`Bloque: ${e.ubicacion_bloque}`, `Aforo: ${e.aforo_maximo}`], tag)
    );
    const op = document.createElement('option');
    op.value = e.id;
    op.textContent = e.nombre;
    select.appendChild(op);
  });
}

async function cargarRecursos() {
  const recursos = await peticion('/recursos/');
  const lista = $('lista-recursos');
  lista.innerHTML = '';
  recursos.forEach((r) => {
    lista.appendChild(
      crearCard(r.nombre_equipo, [
        `Código: ${r.codigo_inventario}`,
        `Costo: S/ ${r.costo_alquiler}`,
        `Stock: ${r.cantidad_stock}`,
        `Espacio: ${r.espacio_detalle.nombre}`,
      ])
    );
  });
}

async function refrescar() {
  try {
    await cargarEspacios();
    await cargarRecursos();
  } catch (e) {
    mostrarAlerta('No se pudo cargar los datos: ' + e.message, 'error');
  }
}

$('form-login').addEventListener('submit', async (ev) => {
  ev.preventDefault();
  try {
    const data = await peticion('/login/', 'POST', {
      username: $('login-user').value,
      password: $('login-pass').value,
    });
    localStorage.setItem('token', data.token);
    $('form-login').reset();
    actualizarSesion();
    mostrarAlerta('Sesión iniciada correctamente.', 'exito');
  } catch (e) {
    mostrarAlerta('Login fallido: ' + e.message, 'error');
  }
});

$('btn-logout').addEventListener('click', () => {
  localStorage.removeItem('token');
  actualizarSesion();
  mostrarAlerta('Sesión cerrada.', 'exito');
});

$('form-espacio').addEventListener('submit', async (ev) => {
  ev.preventDefault();
  try {
    await peticion('/espacios/', 'POST', {
      nombre: $('e-nombre').value,
      ubicacion_bloque: $('e-ubicacion').value,
      aforo_maximo: Number($('e-aforo').value),
      estado_operativo: $('e-estado').checked,
    });
    ev.target.reset();
    mostrarAlerta('Espacio registrado con éxito.', 'exito');
    refrescar();
  } catch (e) {
    mostrarAlerta(`Error (${e.status || 'red'}):\n${e.message}`, 'error');
  }
});

$('form-recurso').addEventListener('submit', async (ev) => {
  ev.preventDefault();
  try {
    await peticion('/recursos/', 'POST', {
      nombre_equipo: $('r-nombre').value,
      codigo_inventario: $('r-codigo').value,
      costo_alquiler: $('r-costo').value,
      cantidad_stock: Number($('r-stock').value),
      espacio: Number($('r-espacio').value),
    });
    ev.target.reset();
    mostrarAlerta('Recurso registrado con éxito.', 'exito');
    refrescar();
  } catch (e) {
    mostrarAlerta(`Error (${e.status || 'red'}):\n${e.message}`, 'error');
  }
});

actualizarSesion();
refrescar();