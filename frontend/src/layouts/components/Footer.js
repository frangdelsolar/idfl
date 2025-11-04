import { Box, Container, Typography } from '@mui/material';

function Footer() {
    return (
        <Box
            component="footer"
            sx={{
                py: 2,
                px: 2,
                backgroundColor: 'white',
                borderTop: '1px solid',
                borderColor: 'divider',
            }}
        >
            <Container maxWidth="lg">
                <Typography
                    variant="body2"
                    color="text.secondary"
                    align="center"
                >
                    © {new Date().getFullYear()} Product Certification System
                </Typography>
            </Container>
        </Box>
    );
}

export default Footer;
