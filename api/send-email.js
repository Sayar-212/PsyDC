const nodemailer = require('nodemailer');

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { clinician, validations } = req.body;

    const transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            user: 'sayar.basu007@gmail.com',
            pass: 'oxjl awia pvbe vlsb'
        }
    });

    const validCount = validations.filter(v => v.validation === 'valid').length;
    const invalidCount = validations.filter(v => v.validation === 'invalid').length;

    const mailOptions = {
        from: 'sayar.basu007@gmail.com',
        to: 'sayar.basu.cse26@heritageit.edu.in',
        subject: `PsyDC Survey Complete - ${clinician}`,
        html: `
            <h2>🎉 Survey Validation Complete!</h2>
            <p><strong>Clinician:</strong> ${clinician}</p>
            <p><strong>Total Reviewed:</strong> ${validations.length}</p>
            <h3>Summary:</h3>
            <ul>
                <li>Valid: ${validCount}</li>
                <li>Invalid: ${invalidCount}</li>
            </ul>
            <h3>Full Results:</h3>
            <pre>${JSON.stringify(validations, null, 2)}</pre>
        `,
        attachments: [{
            filename: `psydc_${clinician}_${Date.now()}.json`,
            content: JSON.stringify({ clinician, validations }, null, 2)
        }]
    };

    try {
        await transporter.sendMail(mailOptions);
        res.status(200).json({ success: true });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
}
