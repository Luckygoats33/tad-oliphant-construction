<?php
require_once __DIR__ . '/resend-config.php';
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: https://tadoliphantconstruction.com');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

$contentType = isset($_SERVER['CONTENT_TYPE']) ? $_SERVER['CONTENT_TYPE'] : '';

if (strpos($contentType, 'application/json') !== false) {
    $raw = file_get_contents('php://input');
    $data = json_decode($raw, true);
} else {
    $data = $_POST;
}

if (empty($data)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'No data received']);
    exit;
}

// Honeypot check
if (!empty($data['_honey'])) {
    echo json_encode(['success' => true]);
    exit;
}

$name    = isset($data['name'])    ? strip_tags(trim($data['name']))    : '';
$phone   = isset($data['phone'])   ? strip_tags(trim($data['phone']))   : '';
$email   = isset($data['email'])   ? filter_var(trim($data['email']), FILTER_SANITIZE_EMAIL) : '';
$service = isset($data['service']) ? strip_tags(trim($data['service'])) : '';
$address = isset($data['address']) ? strip_tags(trim($data['address'])) : '';
$message = isset($data['message']) ? strip_tags(trim($data['message'])) : '';
$source  = isset($data['_source']) ? strip_tags(trim($data['_source'])) : 'Website';
$subject = isset($data['_subject']) ? strip_tags(trim($data['_subject'])) : 'New Estimate Request - Tad Oliphant Construction';

if (empty($name) || empty($phone)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Name and phone are required']);
    exit;
}

$now = new DateTime('now', new DateTimeZone('America/Los_Angeles'));
$dateStr = $now->format('l, F j, Y');
$timeStr = $now->format('g:i A') . ' PT';

$replyLink = $email ? 'mailto:' . htmlspecialchars($email) : '';
$replyLabel = $email ? htmlspecialchars($name) : '';

// --- BRANDED NOTIFICATION EMAIL ---
$notificationHtml = '<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#f4f4f4;font-family:Arial,Helvetica,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:24px 0;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">

<!-- HEADER -->
<tr>
<td style="background:#063E48;padding:28px 32px;text-align:center;">
  <img src="https://tadoliphantconstruction.com/images/logo-new.png" alt="Tad Oliphant Construction" width="72" height="72" style="display:block;margin:0 auto 10px;">
  <div style="margin:0;color:#ffffff;font-size:20px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,Helvetica,sans-serif;">TAD OLIPHANT</div>
  <div style="margin:2px 0 0;color:#E8913A;font-size:15px;font-weight:700;letter-spacing:2px;text-transform:uppercase;font-family:Arial,Helvetica,sans-serif;">CONSTRUCTION</div>
  <div style="margin:14px 0 0;color:#E8913A;font-size:13px;font-weight:600;letter-spacing:0.5px;border-top:1px solid rgba(232,145,58,0.3);padding-top:12px;">New ' . htmlspecialchars($source) . ' Enquiry</div>
</td>
</tr>

<!-- QUICK ACTIONS -->
<tr>
<td style="padding:20px 32px 12px;border-bottom:1px solid #e8e8e8;">';

if ($email) {
    $notificationHtml .= '<a href="' . $replyLink . '" style="display:inline-block;background:#E8913A;color:#ffffff;padding:10px 20px;border-radius:5px;text-decoration:none;font-weight:700;font-size:14px;margin-right:12px;">Reply to ' . $replyLabel . '</a>';
}
$notificationHtml .= '<a href="tel:' . preg_replace('/[^0-9+]/', '', $phone) . '" style="display:inline-block;background:#063E48;color:#ffffff;padding:10px 20px;border-radius:5px;text-decoration:none;font-weight:700;font-size:14px;">Call ' . htmlspecialchars($phone) . '</a>
</td>
</tr>

<!-- FORM DATA TABLE -->
<tr>
<td style="padding:24px 32px;">
<table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">';

$fields = [
    'Name'            => $name,
    'Phone'           => $phone,
    'Email'           => $email,
    'Service Needed'  => $service,
    'Property Address' => $address,
    'Project Details' => $message,
];

$rowNum = 0;
foreach ($fields as $label => $value) {
    if (empty($value)) continue;
    $bg = ($rowNum % 2 === 0) ? '#f9f9f9' : '#ffffff';
    $notificationHtml .= '<tr>
    <td style="padding:12px 16px;background:' . $bg . ';font-weight:700;color:#063E48;font-size:13px;width:140px;vertical-align:top;border-bottom:1px solid #eee;">' . $label . '</td>
    <td style="padding:12px 16px;background:' . $bg . ';color:#333333;font-size:14px;border-bottom:1px solid #eee;">' . nl2br(htmlspecialchars($value)) . '</td>
    </tr>';
    $rowNum++;
}

$notificationHtml .= '</table>
</td>
</tr>

<!-- FOOTER -->
<tr>
<td style="background:#063E48;padding:20px 32px;text-align:center;">
  <p style="margin:0;color:#94b8bf;font-size:12px;">Submitted ' . $dateStr . ' at ' . $timeStr . '</p>
  <p style="margin:6px 0 0;color:#94b8bf;font-size:12px;">via <a href="https://tadoliphantconstruction.com" style="color:#E8913A;text-decoration:none;">tadoliphantconstruction.com</a> &nbsp;&bull;&nbsp; <a href="tel:+15412700274" style="color:#E8913A;text-decoration:none;">(541) 270-0274</a></p>
</td>
</tr>

</table>
</td></tr>
</table>
</body>
</html>';

// --- SEND EMAILS VIA RESEND ---
$resendKey = getenv('RESEND_API_KEY') ?: 're_PLACEHOLDER_SET_ENV_VAR';
$primary = 'will@supportwellnessglobal.com';
$cc = 'oliphant454@yahoo.com';
$fromName = 'Tad Oliphant Construction';
$fromEmail = 'noreply@tadoliphantconstruction.com';

function resend_send($apiKey, $payload) {
    $ch = curl_init('https://api.resend.com/emails');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . $apiKey,
        'Content-Type: application/json'
    ]);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    return ['code' => $httpCode, 'body' => $response];
}

// Send notification to Will + CC Tad
$notifPayload = [
    'from' => "$fromName <$fromEmail>",
    'to' => [$primary],
    'cc' => [$cc],
    'reply_to' => $email ?: $primary,
    'subject' => $subject,
    'html' => $notificationHtml
];

$result = resend_send($resendKey, $notifPayload);
$sent = ($result['code'] >= 200 && $result['code'] < 300);

if ($sent) {
    echo json_encode(['success' => true, 'message' => 'Request received']);
} else {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Failed to send', 'debug' => $result['body']]);
}
