import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import WalletPage from '@/pages/Wallet';
import api from '@/lib/api';

vi.mock('@/lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

function createFakeToken(payload) {
  const encodedPayload = btoa(JSON.stringify(payload));
  return `header.${encodedPayload}.signature`;
}

describe('WalletPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
    localStorage.setItem('token', createFakeToken({ role: 'regular_user', userId: 1 }));
  });

  it('loads and displays the wallet balance', async () => {
    api.get.mockResolvedValueOnce({ data: { walletBalance: 12.5 } });

    render(
      <MemoryRouter>
        <WalletPage />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(api.get).toHaveBeenCalledWith('/wallet/me');
    });

    expect(await screen.findByText(/12\.50/)).toBeInTheDocument();
  });

  it('submits top up and updates wallet balance', async () => {
    const user = userEvent.setup();
    api.get.mockResolvedValueOnce({ data: { walletBalance: 10 } });
    api.post.mockResolvedValueOnce({ data: { walletBalance: 25 } });

    render(
      <MemoryRouter>
        <WalletPage />
      </MemoryRouter>
    );

    const amountInput = await screen.findByLabelText('Amount');
    await user.type(amountInput, '15');
    await user.click(screen.getByRole('button', { name: 'Add Funds' }));

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith('/wallet/top-up', { amount: 15 });
    });

    const successBanner = await screen.findByText(/Wallet updated successfully/i);
    expect(successBanner).toHaveTextContent('$25.00');

    const currentBalanceLabel = screen.getByText('Current Balance');
    expect(currentBalanceLabel.nextElementSibling).toHaveTextContent('$25.00');
  });
});
