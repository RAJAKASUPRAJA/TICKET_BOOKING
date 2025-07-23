document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("bookingForm");
  const fromInput = document.getElementById("origin");
  const toInput = document.getElementById("destination");
  const amountInput = document.getElementById("amount");

  const fareTable = {
    "hyderabad-anantapur": 350,
    "anantapur-hyderabad": 350,
    "hyderabad-bangalore": 550,
    "bangalore-hyderabad": 550,
    "hyderabad-chennai": 700,
    "chennai-hyderabad": 700,
    "anantapur-bangalore": 300,
    "bangalore-anantapur": 300,
  };

  function updateFare() {
    const from = fromInput.value.trim().toLowerCase();
    const to = toInput.value.trim().toLowerCase();
    const key = `${from}-${to}`;
    if (fareTable[key]) {
      amountInput.value = fareTable[key];
    } else {
      amountInput.value = "Invalid route";
    }
  }

  fromInput.addEventListener("input", updateFare);
  toInput.addEventListener("input", updateFare);

  form.addEventListener("submit", (e) => {
    if (amountInput.value === "Invalid route") {
      alert("Please select a valid route before submitting.");
      e.preventDefault();
    }
  });
});
