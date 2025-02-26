# populate_incidents.py

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['incident_response_db']
incidents_collection = db['incidents']

incidents = [
    {
        '_id': str(ObjectId()),
        'incident': 'Phishing email detected. What would you do?',
        'options': ['Report and delete email', 'Ignore and forward it to colleagues', 'Open email and respond'],
        'correct_option': 'Report and delete email',
        'difficulty': 'easy'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'Ransomware detected. How do you proceed?',
        'options': ['Shut down machine', 'Pay ransom', 'Investigate'],
        'correct_option': 'Investigate',
        'difficulty': 'easy'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'Insider threat detected. What steps do you take?',
        'options': ['Monitor', 'Confront', 'Report to HR'],
        'correct_option': 'Report to HR',
        'difficulty': 'medium'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'DDoS attack detected. What’s your first action?',
        'options': ['Block IPs', 'Monitor traffic', 'Scale up bandwidth'],
        'correct_option': 'Monitor traffic',
        'difficulty': 'medium'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'Data breach reported. What’s the first step?',
        'options': ['Forensic analysis', 'Report to authorities', 'Ignore'],
        'correct_option': 'Forensic analysis',
        'difficulty': 'hard'
    },
    
    # Easy level
    {
        '_id': str(ObjectId()),
        'incident': 'What is Phishing?',
        'options': ['An attack that tricks users into providing personal information', 
                    'A type of malware', 
                    'An unauthorized attempt to log into a system', 
                    'A secure method for encrypting passwords'],
        'correct_option': 'An attack that tricks users into providing personal information',
        'difficulty': 'easy'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'What does Malware stand for?',
        'options': ['Malicious Software', 'Malfunctioning Hardware', 'Mass Attackware', 'Managed Alert Response'],
        'correct_option': 'Malicious Software',
        'difficulty': 'easy'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'Which of the following is an example of Multi-Factor Authentication (MFA)?',
        'options': ['Password', 'Security question', 'Password and One-Time Password (OTP)', 'Username'],
        'correct_option': 'Password and One-Time Password (OTP)',
        'difficulty': 'easy'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'What is the main goal of ransomware?',
        'options': ['Encrypt files and demand a ransom', 'Steal personal information', 'Track user behavior', 'Spy on user activities'],
        'correct_option': 'Encrypt files and demand a ransom',
        'difficulty': 'easy'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'What is a firewall used for?',
        'options': ['To block unauthorized access to a network', 'To detect viruses', 'To encrypt data', 'To monitor user activity'],
        'correct_option': 'To block unauthorized access to a network',
        'difficulty': 'easy'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'What does VPN stand for?',
        'options': ['Virtual Private Network', 'Verified Protection Network', 'Virtual Proxy Node', 'Vulnerability Protection Node'],
        'correct_option': 'Virtual Private Network',
        'difficulty': 'easy'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'What is the purpose of a strong password?',
        'options': ['To make it harder for hackers to guess', 'To speed up login times', 'To store more data', 'To bypass encryption'],
        'correct_option': 'To make it harder for hackers to guess',
        'difficulty': 'easy'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'Which of the following is a type of social engineering attack?',
        'options': ['Phishing', 'Brute Force Attack', 'SQL Injection', 'DDoS Attack'],
        'correct_option': 'Phishing',
        'difficulty': 'easy'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'What is a Trojan Horse in cybersecurity?',
        'options': ['A malicious program disguised as legitimate software', 'An attack to overload a network', 'An encrypted virus', 'A type of firewall'],
        'correct_option': 'A malicious program disguised as legitimate software',
        'difficulty': 'easy'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'What is the first step in responding to a security incident?',
        'options': ['Identify the incident', 'Eradicate the threat', 'Notify users', 'Review the logs'],
        'correct_option': 'Identify the incident',
        'difficulty': 'easy'
    },

    # Medium level
    {
        '_id': str(ObjectId()),
        'incident': 'What is the main purpose of an Intrusion Detection System (IDS)?',
        'options': ['To detect unauthorized access to a network', 'To encrypt sensitive data', 'To backup system data', 'To clean malware from infected machines'],
        'correct_option': 'To detect unauthorized access to a network',
        'difficulty': 'medium'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'Which type of malware self-replicates and spreads to other systems?',
        'options': ['Worm', 'Trojan Horse', 'Virus', 'Adware'],
        'correct_option': 'Worm',
        'difficulty': 'medium'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'Which cryptographic method ensures confidentiality?',
        'options': ['Encryption', 'Hashing', 'Tokenization', 'Firewall'],
        'correct_option': 'Encryption',
        'difficulty': 'medium'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'What does the term "zero-day vulnerability" refer to?',
        'options': ['A software vulnerability not yet patched', 'A vulnerability found on the first day of testing', 'A completely secure system', 'A vulnerability already patched'],
        'correct_option': 'A software vulnerability not yet patched',
        'difficulty': 'medium'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'What is the primary goal of penetration testing?',
        'options': ['To find vulnerabilities in a system', 'To optimize software performance', 'To clean infected files', 'To monitor network traffic'],
        'correct_option': 'To find vulnerabilities in a system',
        'difficulty': 'medium'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'What type of attack involves flooding a network with excessive traffic?',
        'options': ['DDoS (Distributed Denial of Service)', 'Phishing', 'Brute Force', 'Man-in-the-Middle'],
        'correct_option': 'DDoS (Distributed Denial of Service)',
        'difficulty': 'medium'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'What is "two-factor authentication"?',
        'options': ['An additional layer of security beyond just a password', 'A security question asked twice', 'Using two passwords to log in', 'Encrypting data with two methods'],
        'correct_option': 'An additional layer of security beyond just a password',
        'difficulty': 'medium'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'What does SSL/TLS stand for in cybersecurity?',
        'options': ['Secure Sockets Layer / Transport Layer Security', 'System Security Layer / Transaction Layer Standard', 'Server Security Link / Transmission Lock System', 'Standard Secure Login / Transport Lock Standard'],
        'correct_option': 'Secure Sockets Layer / Transport Layer Security',
        'difficulty': 'medium'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'What is the first phase in the NIST Incident Response Lifecycle?',
        'options': ['Preparation', 'Containment', 'Recovery', 'Eradication'],
        'correct_option': 'Preparation',
        'difficulty': 'medium'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'Which type of attack intercepts communications between two parties to steal data?',
        'options': ['Man-in-the-Middle Attack', 'SQL Injection', 'DDoS Attack', 'Phishing'],
        'correct_option': 'Man-in-the-Middle Attack',
        'difficulty': 'medium'
    },

    # Difficult level
    {
        '_id': str(ObjectId()),
        'incident': 'Which protocol is primarily used for secure email communications?',
        'options': ['PGP (Pretty Good Privacy)', 'FTP (File Transfer Protocol)', 'SMTP (Simple Mail Transfer Protocol)', 'HTTP (Hypertext Transfer Protocol)'],
        'correct_option': 'PGP (Pretty Good Privacy)',
        'difficulty': 'hard'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'What is the main focus of the CIS Control #1 in the CIS Critical Security Controls?',
        'options': ['Inventory and Control of Hardware Assets', 'Secure Configuration for Hardware', 'Data Protection', 'Email and Web Browser Protections'],
        'correct_option': 'Inventory and Control of Hardware Assets',
        'difficulty': 'hard'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'Which hashing algorithm is no longer considered secure due to vulnerabilities?',
        'options': ['MD5', 'SHA-256', 'HMAC', 'AES'],
        'correct_option': 'MD5',
        'difficulty': 'hard'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'Which cybersecurity framework is most commonly used for risk management?',
        'options': ['NIST Cybersecurity Framework', 'OWASP Top Ten', 'PCI-DSS', 'HIPAA'],
        'correct_option': 'NIST Cybersecurity Framework',
        'difficulty': 'hard'
    },
    {
        '_id': str(ObjectId()),
        'incident': 'Zero-day vulnerability exploited. What do you do?',
        'options': ['Patch', 'Shutdown', 'Public statement'],
        'correct_option': 'Patch',
        'difficulty': 'hard'
    }
    
]

incidents_collection.insert_many(incidents)
print("Incidents inserted successfully!")
