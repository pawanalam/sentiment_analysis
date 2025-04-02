// ProfileForm.jsx
import { useState } from "react";
import axios from "axios";
import "../app.css";

const ProfileForm = ({ setResult }) => {
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        contact: "",
        linkedin: "",
        github: "",
        resume: null
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleFileChange = (e) => {
        setFormData({ ...formData, resume: e.target.files[0] });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!formData.name || !formData.email || !formData.contact) return;

        console.log("\ud83d\udce4 Sending Form Data:", formData);

        const formDataToSend = new FormData();
        Object.keys(formData).forEach((key) => {
            if (key === "resume" && formData[key]) {
                formDataToSend.append(key, formData[key], formData[key].name);
            } else {
                formDataToSend.append(key, formData[key]);
            }
        });

        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/api/data/",
                formDataToSend,
                {
                    headers: { "Content-Type": "multipart/form-data" },
                    withCredentials: true,  // ✅ REQUIRED to send cookies for session tracking
                }
            );            
        } catch (error) {
            console.error("\u274c Error submitting data:", error.response?.data || error.message);
            setResult({ error: "Failed to submit the form" });
        }
    };

    return (
        <div>
            <h1>InsightsLens.AI</h1>
            <h2>Profile Submission</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
                <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
                <input type="tel" name="contact" placeholder="Contact No." value={formData.contact} onChange={handleChange} required />
                <input type="url" name="linkedin" placeholder="LinkedIn URL" value={formData.linkedin} onChange={handleChange} />
                <input type="url" name="github" placeholder="GitHub URL" value={formData.github} onChange={handleChange} />
                <input type="file" name="resume" accept="application/pdf" onChange={handleFileChange} />
                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default ProfileForm;