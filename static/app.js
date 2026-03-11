const API_BASE = "";

let currentFilter = "all";

const $form = document.getElementById("todo-form");
const $title = document.getElementById("todo-title");
const $desc = document.getElementById("todo-desc");
const $list = document.getElementById("todo-list");
const $empty = document.getElementById("empty-state");
const $filters = document.querySelectorAll(".filters button");

function showError(msg) {
  let el = document.querySelector(".error-message");
  if (!el) {
    el = document.createElement("p");
    el.className = "error-message";
    document.querySelector(".app").insertBefore(el, document.querySelector(".filters"));
  }
  el.textContent = msg;
  el.classList.remove("hidden");
  setTimeout(() => el.classList.add("hidden"), 4000);
}

async function api(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText || "Request failed");
  }
  if (res.status === 204) return null;
  return res.json();
}

function renderTodo(todo) {
  const li = document.createElement("li");
  li.className = "todo-item" + (todo.completed ? " completed" : "");
  li.dataset.id = todo.id;
  li.innerHTML = `
    <input type="checkbox" class="todo-check" ${todo.completed ? "checked" : ""} aria-label="Toggle completed" />
    <div class="todo-content">
      <p class="todo-title">${escapeHtml(todo.title)}</p>
      ${todo.description ? `<p class="todo-desc">${escapeHtml(todo.description)}</p>` : ""}
    </div>
    <div class="todo-actions">
      <button type="button" class="delete" aria-label="Delete">Delete</button>
    </div>
  `;
  const checkbox = li.querySelector(".todo-check");
  const deleteBtn = li.querySelector(".delete");
  checkbox.addEventListener("change", () => toggleTodo(todo.id, checkbox.checked));
  deleteBtn.addEventListener("click", () => deleteTodo(todo.id));
  return li;
}

function escapeHtml(s) {
  const div = document.createElement("div");
  div.textContent = s;
  return div.innerHTML;
}

function filterTodos(todos) {
  if (currentFilter === "active") return todos.filter((t) => !t.completed);
  if (currentFilter === "completed") return todos.filter((t) => t.completed);
  return todos;
}

async function loadTodos() {
  try {
    const todos = await api("/api/todos");
    $list.innerHTML = "";
    const filtered = filterTodos(todos);
    filtered.forEach((todo) => $list.appendChild(renderTodo(todo)));
    $empty.classList.toggle("hidden", filtered.length > 0);
  } catch (e) {
    showError(e.message || "Failed to load todos");
  }
}

async function createTodo(title, description) {
  await api("/api/todos", {
    method: "POST",
    body: JSON.stringify({ title, description: description || "", completed: false }),
  });
  await loadTodos();
}

async function toggleTodo(id, completed) {
  try {
    await api(`/api/todos/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ completed }),
    });
    await loadTodos();
  } catch (e) {
    showError(e.message || "Failed to update");
    await loadTodos();
  }
}

async function deleteTodo(id) {
  try {
    await api(`/api/todos/${id}`, { method: "DELETE" });
    await loadTodos();
  } catch (e) {
    showError(e.message || "Failed to delete");
    await loadTodos();
  }
}

$form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = $title.value.trim();
  if (!title) return;
  $form.classList.add("loading");
  try {
    await createTodo(title, $desc.value.trim());
    $title.value = "";
    $desc.value = "";
    $title.focus();
  } catch (e) {
    showError(e.message || "Failed to add todo");
  } finally {
    $form.classList.remove("loading");
  }
});

$filters.forEach((btn) => {
  btn.addEventListener("click", () => {
    $filters.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    currentFilter = btn.dataset.filter;
    loadTodos();
  });
});

loadTodos();
