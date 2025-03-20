export default function Pagination({ onPageChange, currentPage, totalPages }) {
  return (
    <div>
      <p>Current Page: {currentPage}</p>
      <p>Total Pages: {totalPages}</p>
    </div>
  );
}
