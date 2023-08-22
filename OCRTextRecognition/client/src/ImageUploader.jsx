import React, { useState } from 'react';

function ImageSubmitForm() {
  const [selectedImage, setSelectedImage] = useState(null);

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    setSelectedImage(URL.createObjectURL(file));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Perform any necessary actions with the selected image here
    // For example, send it to a server or process it further
    // Reset the form and selected image state
    setSelectedImage(null);
    event.target.reset();
  };

  return (
    <div>
      <h2>Image Submit Form</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="imageUpload">Select an image:</label>
          <input
            type="file"
            id="imageUpload"
            accept=".jpg, .jpeg, .png"
            onChange={handleImageChange}
            required
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      {selectedImage && (
        <div>
          <h3>Selected Image:</h3>
          <img src={selectedImage} alt="Selected" style={{ maxWidth: '100%', marginTop: '10px' }} />
        </div>
      )}
    </div>
  );
}

export default ImageSubmitForm;
