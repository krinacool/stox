document.addEventListener('DOMContentLoaded', function () {
    const secretKeyInput = document.getElementById('id_secret_key');
    const redirectUriInput = document.getElementById('id_redirect_uri');
    const copyButton = document.createElement('button');

    copyButton.type = 'button';
    copyButton.innerText = 'Copy Redirect URI';
    copyButton.style.marginLeft = '10px';

    redirectUriInput.parentNode.appendChild(copyButton);

    function updateRedirectUri() {
        const secretKey = secretKeyInput.value;
        const newRedirectUri = `https://onstock.in/upstox_cred/${secretKey}`;
        redirectUriInput.value = newRedirectUri;
    }

    secretKeyInput.addEventListener('input', updateRedirectUri);

    copyButton.addEventListener('click', function () {
        navigator.clipboard.writeText(redirectUriInput.value).then(function () {
            alert('Redirect URI copied to clipboard');
        }, function (err) {
            console.error('Could not copy text: ', err);
        });
    });

    // Initialize the redirect URI on page load
    updateRedirectUri();
});
